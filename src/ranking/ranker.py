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

                honeypot_penalty = (
                    self.honeypot_detector.detect(
                        candidate,
                        candidate_features
                    )
                )

                honeypot_time += (
                    time.time() - t0
                )

                candidate_features[
                    "honeypot_penalty"
                ] = honeypot_penalty

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
        k=100
    ):

        ranking_start = time.time()

        ranked = self.rank_candidates(
            candidates
        )

        # ==========================
        # Top-K Selection
        # ==========================

        topk_start = time.time()

        ranked = heapq.nlargest(

            k,

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
