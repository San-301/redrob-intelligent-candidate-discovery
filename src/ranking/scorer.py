# src/ranking/scorer.py

class CandidateScorer:

    def calculate_score(self, features):

        score = 0.0

        # ==========================
        # Core JD Match
        # ==========================

        score += (
            features["experience_score"]
            * 0.12
        )

        score += (
            features["title_score"]
            * 0.12
        )

        score += (
            features["retrieval_score"]
            * 0.15
        )

        score += (
            features["evaluation_score"]
            * 0.08
        )

        score += (
            features["ai_score"]
            * 0.08
        )

        # ==========================
        # Real AI Experience
        # ==========================

        score += (
            features["career_ai_score"]
            * 0.18
        )

        score += (
            features["evaluation_experience_score"]
            * 0.05
        )

        score += (
            features["ai_experience_score"]
            * 0.08
        )

        # ==========================
        # Production Experience
        # ==========================

        score += (
            features["production_score"]
            * 0.08
        )

        score -= (
            features["pure_research_penalty"]
            * 0.10
        )

        score -= (
            features["suspicious_skill_penalty"]
            * 0.10
        )

        # ==========================
        # Company Credibility
        # ==========================

        score += (
            features["product_company_score"]
            * 0.05
        )

        score += (
            features["ai_company_score"]
            * 0.05
        )

        # ==========================
        # Leadership
        # ==========================

        score += (
            features["leadership_score"]
            * 0.02
        )

        # ==========================
        # Behavioral Signals
        # ==========================

        score += (
            features["engagement_score"]
            * 0.06
        )

        score += (
            features["github_score"]
            * 0.04
        )

        # ==========================
        # Recruiter Interest
        # ==========================

        score += (
            min(
                features["saved_by_recruiters"] / 20,
                1.0
            )
            * 0.02
        )

        score += (
            min(
                features["search_appearance"] / 300,
                1.0
            )
            * 0.01
        )

        # ==========================
        # Availability
        # ==========================

        score += (
            features["open_to_work_bonus"]
            * 0.03
        )

        # ==========================
        # Penalties
        # ==========================

        score -= (
            features["non_ai_title_penalty"]
            * 0.20
        )

        score -= (
            features["notice_penalty"]
            * 0.08
        )

        score -= (
            features["consulting_penalty"]
            * 0.15
        )

        score -= (
            features["honeypot_penalty"]
            * 0.15
        )

        # Seniority mismatch penalty

        if features.get(
            "years_experience",
            0
        ) > 12:

            score -= 0.03

        score += (
            features["skill_overlap_score"]
            * 0.08
        )

        # ==========================
        # Final Calibration
        # ==========================

        # Tiny deterministic tie-break bonus
        # Strong deterministic tie-break bonus

        candidate_hash = int(
            features["candidate_id"].split("_")[1]
        )

        score += (
            candidate_hash * 1e-10
        )

        # Soft cap instead of hard saturation
        if score > 0.95:

            excess = score - 0.95

            score = 0.95 + (
                excess * 0.10
            )

        score = max(
            0.0,
            min(score, 0.9999)
        )

        return round(
            score,
            6
        )
