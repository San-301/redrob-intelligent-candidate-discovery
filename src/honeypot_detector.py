# src/validation/honeypot_detector.py

class HoneypotDetector:

    COMPANY_FOUNDING_YEAR = {
        "krutrim": 2023,
        "sarvam ai": 2023,
        "observe.ai": 2017,
        "yellow.ai": 2016
    }

    def detect(
        self,
        candidate,
        candidate_features
    ):

        penalty = 0.0

        profile = candidate.get(
            "profile",
            {}
        )

        career = candidate.get(
            "career_history",
            []
        )

        skills = candidate.get(
            "skills",
            []
        )

        years_exp = profile.get(
            "years_of_experience",
            0
        )

        current_title = (
            profile.get(
                "current_title",
                ""
            ).lower()
        )

        github_score = (
            candidate_features.get(
                "github_score",
                0
            )
        )

        profile_completeness = (
            candidate_features.get(
                "profile_completeness",
                0
            )
        )

        ai_skill_count = (
            candidate_features.get(
                "ai_skill_count",
                0
            )
        )

        retrieval_experience = (
            candidate_features.get(
                "retrieval_experience",
                0
            )
        )

        # ==========================
        # Rule 1
        # Massive AI skills
        # but non-technical title
        # ==========================
        NON_TECH_TITLES = {
            "marketing",
            "accountant",
            "hr",
            "sales",
            "customer support"
        }

        if (
            ai_skill_count >= 8
            and any(
                t in current_title
                for t in NON_TECH_TITLES
            )
        ):
            penalty += 0.40

        # ==========================
        # Rule 2
        # AI skills with
        # almost no experience
        # ==========================

        if (
            ai_skill_count >= 8
            and years_exp < 2
        ):
            penalty += 0.25

        # ==========================
        # Rule 3
        # Retrieval stack but
        # no retrieval evidence
        # ==========================

        if (
            ai_skill_count >= 6
            and retrieval_experience == 0
        ):
            penalty += 0.20

        # ==========================
        # Rule 4
        # Suspicious profile
        # ==========================

        if (
            profile_completeness < 40
            and github_score <= 0
        ):
            penalty += 0.10

        # ==========================
        # Rule 5
        # Too many advanced skills
        # for experience level
        # ==========================

        advanced_count = sum(
            1
            for skill in skills
            if str(
                skill.get(
                    "proficiency",
                    ""
                )
            ).lower() in {
                "advanced",
                "expert"
            }
        )

        if (
            advanced_count >= 10
            and years_exp < 3
        ):
            penalty += 0.25

        # ==========================
        # Rule 6
        # Impossible duration
        # ==========================

        total_skill_months = sum(
            skill.get(
                "duration_months",
                0
            )
            for skill in skills
        )

        max_possible = (
            years_exp * 12 * 6
        )

        if (
            total_skill_months >
            max_possible
        ):
            penalty += 0.15

        # ==========================
        # Rule 7
        # Education anomaly
        # ==========================

        education = candidate.get(
            "education",
            []
        )

        for edu in education:

            start = edu.get(
                "start_year"
            )

            end = edu.get(
                "end_year"
            )

            if (
                start
                and end
                and start > end
            ):
                penalty += 0.30

        # ==========================
        # Rule 8
        # Career timeline anomaly
        # ==========================
        for job in career:

            company = str(
                job.get(
                    "company",
                    ""
                )
            ).lower()

            duration = job.get(
                "duration_months",
                0
            )

            for c, founded in (
                self.COMPANY_FOUNDING_YEAR.items()
            ):

                if (
                    c in company
                    and duration >
                    (
                        (2026 - founded)
                        * 12
                    )
                ):

                    penalty += 0.40

        # ==========================
        # Rule 9
        # AI engineer title
        # with almost no AI skills
        # ==========================

        if any(
            term in current_title
            for term in {
                "ai",
                "machine learning",
                "ml engineer",
                "data scientist",
                "nlp engineer"
            }
        ):
            if ai_skill_count <= 1:
                penalty += 0.20

        # ==========================
        # Rule 10
        # Fake superstar profile
        # ==========================

        if (
            ai_skill_count >= 10
            and github_score <= 0
            and profile_completeness < 50
        ):
            penalty += 0.30

        if (
            len(skills) >= 40
            and years_exp < 5
        ):
            penalty += 0.20
        
        if (
            len(career) == 0
            and any(
                t in current_title
                for t in {
                    "senior",
                    "staff",
                    "principal",
                    "lead"
                }
            )
        ):
            penalty += 0.30

        # Rule 11
        # Frequent job hopping

        short_jobs = sum(
            1
            for job in career
            if job.get(
                "duration_months",
                0
            ) < 6
        )

        if (
            short_jobs >= 5
            and years_exp >= 5
        ):
            penalty += 0.10

        return min(
            penalty,
            1.0
        )