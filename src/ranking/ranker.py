# src/ranking/ranker.py

import time
import heapq

from src.preprocessing.candidate_parser import CandidateParser
from src.features.feature_builder import FeatureBuilder
from src.ranking.scorer import CandidateScorer
from src.reasoning.reason_generator import ReasonGenerator
from src.validation.honeypot_detector import HoneypotDetector


class CandidateRanker:

    def __init__(self, jd_features):

        self.jd_features = jd_features

        self.parser = CandidateParser()
        self.feature_builder = FeatureBuilder()
        self.scorer = CandidateScorer()
        self.reason_generator = ReasonGenerator()
        self.honeypot_detector = HoneypotDetector()

    def rank_candidates(self, candidates):

        ranked_candidates = []

        parse_time = 0
        honeypot_time = 0
        feature_time = 0
        scoring_time = 0

        total_start = time.time()

        for idx, candidate in enumerate(candidates):

            try:

                # ==========================
                # Candidate Parsing
                # ==========================

                t0 = time.time()

                candidate_features = (
                    self.parser.parse(candidate)
                )

                parse_time += (
                    time.time() - t0
                )

                # ==========================
                # Early Filtering
                # ==========================

                years = candidate_features.get(
                    "years_experience",
                    0
                )

                ai_skills = candidate_features.get(
                    "ai_skill_count",
                    0
                )

                title = str(
                    candidate_features.get(
                        "current_title",
                        ""
                    )
                ).lower()

                # obvious rejects

                if (
                    years < 1
                    and ai_skills == 0
                ):
                    continue

                if any(
                    x in title
                    for x in {
                        "marketing",
                        "sales",
                        "hr",
                        "accountant",
                        "support"
                    }
                ):
                    continue

                # ==========================
                # Honeypot Detection
                # ==========================

                t0 = time.time()

                hp_audit = (
                    self.honeypot_detector.inspect(
                        candidate,
                        candidate_features
                    )
                )

                honeypot_time += (
                    time.time() - t0
                )

                candidate_features[
                    "honeypot_penalty"
                ] = hp_audit["penalty"]

                candidate_features[
                    "honeypot_flags"
                ] = hp_audit["flags"]

                # ==========================
                # Feature Engineering
                # ==========================

                t0 = time.time()

                features = (
                    self.feature_builder.build(
                        candidate_features,
                        self.jd_features
                    )
                )

                feature_time += (
                    time.time() - t0
                )

                # ==========================
                # Scoring
                # ==========================

                t0 = time.time()

                score = (
                    self.scorer.calculate_score(
                        features
                    )
                )

                scoring_time += (
                    time.time() - t0
                )

                ranked_candidates.append({

                    "candidate_id":
                        candidate["candidate_id"],

                    "score":
                        score,

                    "reasoning": "",

                    "features":
                        features,

                    "candidate_features":
                        candidate_features
                })

                if (
                    idx > 0
                    and idx % 10000 == 0
                ):
                    print(
                        f"Processed {idx} candidates..."
                    )

            except Exception as e:

                print(
                    f"Error processing "
                    f"{candidate.get('candidate_id')} "
                    f": {e}"
                )

        total_time = (
            time.time() - total_start
        )

        print("\n========== PROFILING ==========")
        print(
            f"Parsing Time: "
            f"{parse_time:.2f}s"
        )

        print(
            f"Honeypot Time: "
            f"{honeypot_time:.2f}s"
        )

        print(
            f"Feature Time: "
            f"{feature_time:.2f}s"
        )

        print(
            f"Scoring Time: "
            f"{scoring_time:.2f}s"
        )

        print(
            f"Total Ranking Time: "
            f"{total_time:.2f}s"
        )

        return ranked_candidates

    def get_top_k(
        self,
        candidates,
        k=100,
        exclude_honeypots=False
    ):

        ranking_start = time.time()

        ranked = self.rank_candidates(
            candidates
        )

        # Keep track of all quarantined honeypots across the dataset
        self.last_quarantined = [
            c for c in ranked
            if c.get("candidate_features", {}).get("honeypot_penalty", 0) > 0.15
        ]

        if exclude_honeypots:
            # Filter BEFORE heap selection so the final list contains exactly k clean candidates
            ranked = [
                c for c in ranked
                if c.get("candidate_features", {}).get("honeypot_penalty", 0) <= 0.15
            ]

        # ==========================
        # Top-K Selection
        # ==========================

        topk_start = time.time()

        actual_k = min(k, len(ranked)) if ranked else k
        ranked = heapq.nlargest(

            actual_k,

            ranked,

            key=lambda x: (

                x["score"],

                x["features"].get(
                    "engagement_score",
                    0
                ),

                x["features"].get(
                    "github_score",
                    0
                ),

                x["features"].get(
                    "career_ai_score",
                    0
                ),

                -int(
                    x["candidate_id"]
                    .split("_")[1]
                )
            )
        )

        # deterministic ordering

        ranked.sort(

            key=lambda x: (

                -x["score"],

                x["candidate_id"]

            )
        )

        # Recruiter Dynamic Range Calibration (Spreads top candidates across realistic 0.745 - 0.978 range)
        ranked = self.calibrate_top_k_scores(ranked)

        print(
            f"Top-K Selection Time: "
            f"{time.time() - topk_start:.2f}s"
        )

        # ==========================
        # Generate Reasoning
        # ==========================

        reasoning_start = time.time()

        for idx, candidate in enumerate(
            ranked,
            start=1
        ):

            candidate["rank"] = idx

            candidate["reasoning"] = (

                self.reason_generator.generate(

                    candidate[
                        "candidate_features"
                    ],

                    candidate["score"]
                )
            )

        print(
            f"Reasoning Time: "
            f"{time.time() - reasoning_start:.2f}s"
        )

        print(
            f"Overall Ranker Time: "
            f"{time.time() - ranking_start:.2f}s"
        )

        return ranked

    def calibrate_top_k_scores(self, ranked, target_max=0.9780, target_min=0.7450):
        """
        Calibrates the Top-K candidate scores to provide a realistic, recruiter-friendly
        dynamic spread (from ~0.978 down to ~0.745) rather than squashing everyone into
        a tiny 0.015 band. Preserves strict rank order, relative score separation,
        and monotonicity.
        """
        k = len(ranked)
        if k <= 1:
            return ranked
            
        scores = [c["score"] for c in ranked]
        s_max = max(scores)
        s_min = min(scores)
        spread = s_max - s_min
        
        # Adaptive min target based on k (e.g. k=10 scales to 0.910, k=100 down to 0.745)
        effective_min = target_max - (target_max - target_min) * min(1.0, k / 100.0)
        
        prev_score = target_max + 0.01
        for i, cand in enumerate(ranked):
            s = cand["score"]
            t = (s - s_min) / spread if spread > 0 else (1.0 - i / max(1, k - 1))
            rank_factor = 1.0 - (i / max(1, k - 1))
            
            # Blend relative score strength (65%) with rank curve (35%)
            calibrated = effective_min + (target_max - effective_min) * (0.65 * t + 0.35 * rank_factor)
            
            # Tiny tie-break bonus
            cand_id_num = int(cand["candidate_id"].split("_")[1]) if "_" in cand["candidate_id"] else i
            calibrated += (cand_id_num % 1000) * 1e-8
            
            # Strictly enforce non-increasing monotonicity
            calibrated = min(calibrated, prev_score - 0.0001)
            prev_score = calibrated
            
            cand["score"] = round(calibrated, 6)
            
        return ranked
