# src/reasoning/reason_generator.py

class ReasonGenerator:

    def generate(
        self,
        candidate_features,
        final_score
    ):

        strengths = []
        concerns = []

        exp = candidate_features.get(
            "years_experience",
            0
        )

        title = candidate_features.get(
            "current_title",
            ""
        )

        strengths.append(
            f"{exp:.1f} years experience as {title}"
        )

        # Retrieval / Search
        if candidate_features.get(
            "retrieval_skill_count",
            0
        ) >= 3:

            strengths.append(
                "strong retrieval/search background"
            )

        elif candidate_features.get(
            "retrieval_experience",
            0
        ):

            strengths.append(
                "some retrieval exposure"
            )

        # AI Skills
        ai_count = candidate_features.get(
            "ai_skill_count",
            0
        )

        if ai_count >= 8:

            strengths.append(
                "extensive AI/ML skill coverage"
            )

        elif ai_count >= 4:

            strengths.append(
                "relevant AI/ML experience"
            )

        # Evaluation
        if candidate_features.get(
            "evaluation_skill_count",
            0
        ) > 0:

            strengths.append(
                "evaluation/ranking knowledge"
            )

        # Product Company
        if candidate_features.get(
            "product_company_exp",
            0
        ) > 0:

            strengths.append(
                "product-company background"
            )

        # AI Company
        if candidate_features.get(
            "ai_company_exp",
            0
        ) > 0:

            strengths.append(
                "worked in AI-focused company"
            )

        # Leadership
        if candidate_features.get(
            "production_score",
            0
        ) >= 0.5:

            strengths.append(
                "evidence of production-scale ML systems"
            )
        if candidate_features.get(
            "recent_activity_score",
            0
        ) >= 0.8:

            strengths.append(
                "recently active on platform"
            )
            
        if candidate_features.get(
            "leadership_score",
            0
        ) >= 0.5:

            strengths.append(
                "leadership and ownership signals"
            )

        # Recruiter Interest
        if candidate_features.get(
            "saved_by_recruiters",
            0
        ) >= 10:

            strengths.append(
                "high recruiter interest"
            )

        # GitHub
        github = candidate_features.get(
            "github_score",
            0
        )

        if github >= 50:

            strengths.append(
                "strong GitHub activity"
            )

        elif github <= 0:

            concerns.append(
                "no GitHub activity signal"
            )

        # Open to Work
        if candidate_features.get(
            "open_to_work",
            0
        ):

            strengths.append(
                "actively open to work"
            )

        # Notice Period
        notice = candidate_features.get(
            "notice_period",
            0
        )

        if notice > 90:

            concerns.append(
                f"long notice period ({notice} days)"
            )

        # Consulting-only
        if candidate_features.get(
            "consulting_only",
            0
        ):

            concerns.append(
                "primarily consulting background"
            )

        if candidate_features.get(
            "career_ai_score",
            0
        ) >= 0.7:

            strengths.append(
                "strong evidence of real-world AI projects"
            )

        elif candidate_features.get(
            "career_ai_score",
            0
        ) >= 0.3:

            strengths.append(
                "some applied AI project experience"
            )
        
        if (
            candidate_features.get(
                "production_score",
                0
            ) < 0.2
            and candidate_features.get(
                "years_experience",
                0
            ) >= 5
        ):
            concerns.append(
                "limited evidence of production deployments"
            )

        if candidate_features.get(
            "suspicious_skill_penalty",
            0
        ) >= 0.6:

            concerns.append(
                "skill claims appear inflated"
            )

        if candidate_features.get(
            "pure_research_penalty",
            0
        ):

            concerns.append(
                "profile appears research-heavy with limited production evidence"
            )

        # Honeypot Risk
        if candidate_features.get(
            "honeypot_penalty",
            0
        ) > 0.3:

            concerns.append(
                "profile consistency concerns"
            )

        if candidate_features.get(
            "honeypot_penalty",
            0
        ) >= 0.5:

            concerns.insert(
                0,
                "multiple profile inconsistencies detected"
            )

        # Build Final Reasoning

        strengths = list(dict.fromkeys(strengths))

        # prioritize diverse strengths

        priority_order = [
            "evidence of production-scale ML systems",
            "strong evidence of real-world AI projects",
            "some applied AI project experience",
            "strong retrieval/search background",
            "evaluation/ranking knowledge",
            "product-company background",
            "worked in AI-focused company",
            "leadership and ownership signals",
            "high recruiter interest",
            "strong GitHub activity",
            "recently active on platform",
            "actively open to work",
            "extensive AI/ML skill coverage",
            "relevant AI/ML experience",
        ]

        ordered_strengths = []

        for p in priority_order:
            if p in strengths:
                ordered_strengths.append(p)

        for s in strengths:
            if s not in ordered_strengths:
                ordered_strengths.append(s)

        final_strengths = []

        # Always keep years/title first
        final_strengths.append(
            strengths[0]
        )

        for s in ordered_strengths:
            if s not in final_strengths:
                final_strengths.append(s)

        strengths_text = ", ".join(
            final_strengths[:4]
        )

        if final_score >= 0.96:
            prefix = "Excellent match: "

        elif final_score >= 0.88:
            prefix = "Strong match: "

        elif final_score >= 0.78:
            prefix = "Good match: "

        else:
            prefix = "Potential match: "
        reasoning = prefix + strengths_text

        if final_score >= 0.96:
            reasoning += (
                "; exceptional fit for retrieval and ranking ownership"
            )

        elif final_score >= 0.88:
            reasoning += (
                "; strong fit for retrieval and ranking ownership"
            )

        elif final_score >= 0.78:
            reasoning += (
                "; aligns well with core JD requirements"
            )

        else:
            reasoning += (
                "; adjacent profile with notable gaps"
            )
        concerns = list(dict.fromkeys(concerns))

        if concerns:

            reasoning += (
                ". Concerns: "
                + ", ".join(concerns[:2])
            )
        reasoning += (
            f". Signals: GitHub "
            f"{candidate_features.get('github_score', 0):.1f}, "
            f"response "
            f"{candidate_features.get('response_rate', 0) * 100:.0f}%, "
            f"ref {candidate_features['candidate_id'][-4:]}"
        )

        return reasoning