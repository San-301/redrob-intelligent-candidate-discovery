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
        return self.inspect(candidate, candidate_features)["penalty"]

    def inspect(
        self,
        candidate,
        candidate_features
    ):
        penalty = 0.0
        flags = []

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

        retrieval_skill_count = (
            candidate_features.get(
                "retrieval_skill_count",
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
            flags.append("Rule 1: Non-technical title claiming excessive AI skills")

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
            flags.append("Rule 2: High AI skill claims with under 2 years total experience")

        # ==========================
        # Rule 3
        # Retrieval tools claimed in skills
        # but zero applied project evidence
        # ==========================

        if (
            retrieval_skill_count >= 2
            and candidate_features.get("career_ai_score", 0) == 0
        ):
            penalty += 0.20
            flags.append("Rule 3: Claimed retrieval/vector stack with zero applied AI project evidence")

        # ==========================
        # Rule 4
        # Suspicious profile
        # ==========================

        if (
            profile_completeness < 40
            and github_score <= 0
        ):
            penalty += 0.10
            flags.append("Rule 4: Low profile completeness with zero developer activity")

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
            flags.append("Rule 5: Unrealistic number of expert skills for junior profile")

        # ==========================
        # Rule 6
        # Impossible skill duration
        # ==========================

        career_months_limit = (years_exp * 12) + 12

        # 6a: A single skill's claimed duration cannot exceed total career experience
        impossible_single_skill = any(
            skill.get("duration_months", 0) > career_months_limit
            for skill in skills
            if years_exp >= 1
        )

        total_skill_months = sum(
            skill.get("duration_months", 0)
            for skill in skills
        )

        # 6b: Gross inflation: Real engineers use ~15 parallel skills (languages, frameworks, DBs, cloud).
        # Flag only when claimed skills exceed 22x parallel full-time tenure.
        max_possible_cumulative = max(years_exp * 12 * 22, 360)

        if impossible_single_skill:
            penalty += 0.20
            flags.append("Rule 6: Claimed skill duration exceeds total career experience")
        elif total_skill_months > max_possible_cumulative and years_exp >= 1:
            penalty += 0.15
            flags.append("Rule 6: Grossly inflated cumulative skill duration (>22 parallel skills claimed)")

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
                flags.append(f"Rule 7: Inverted education timeline (start {start} > end {end})")

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
                    flags.append(f"Rule 8: Experience duration at {c.title()} exceeds company existence (founded {founded})")

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
                flags.append("Rule 9: AI/ML title with almost no reported AI skills")

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
            flags.append("Rule 10: Fake superstar profile (high skills, 0 GitHub, low completeness)")

        if (
            len(skills) >= 40
            and years_exp < 5
        ):
            penalty += 0.20
            flags.append("Rule 10b: Skill stuffing (40+ skills with under 5 years experience)")
        
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
            flags.append("Rule 10c: Senior title with zero career history records")

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
            flags.append("Rule 11: Frequent short-term job hopping (5+ jobs < 6 months)")

        return {
            "penalty": min(penalty, 1.0),
            "flags": flags,
            "is_suspicious": penalty > 0.0
        }
