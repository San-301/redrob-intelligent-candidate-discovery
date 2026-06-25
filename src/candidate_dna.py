from typing import Dict


class CandidateDNA:

    RETRIEVAL_TERMS = {
        "retrieval",
        "search",
        "ranking",
        "recommendation",
        "recommendation systems",
        "semantic search",
        "vector search",
        "information retrieval",
        "embeddings",
        "faiss",
        "qdrant",
        "pinecone",
        "weaviate",
        "milvus",
        "bm25",
        "elasticsearch",
        "opensearch"
    }

    EVALUATION_TERMS = {
        "ndcg",
        "mrr",
        "map",
        "ab test",
        "a/b test",
        "evaluation",
        "offline benchmark",
        "ranking metrics",
        "precision",
        "recall"
    }

    PRODUCT_COMPANIES = {
        "google",
        "amazon",
        "meta",
        "microsoft",
        "linkedin",
        "uber",
        "zomato",
        "swiggy",
        "flipkart",
        "phonepe",
        "cred",
        "razorpay",
        "ola",
        "meesho",
        "freshworks",
        "zoho",
        "dream11",
        "nykaa",
        "paytm",
        "observe.ai",
        "yellow.ai",
        "sarvam ai",
        "krutrim",
        "haptik",
        "mad street den"
    }

    AI_COMPANIES = {
        "observe.ai",
        "yellow.ai",
        "sarvam ai",
        "krutrim",
        "haptik",
        "mad street den",
        "rephrase.ai",
        "aganitha",
        "wysa"
    }

    def build(self, candidate: Dict) -> Dict:

        profile = candidate.get("profile", {})
        career = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})

        text_parts = []

        text_parts.append(
            profile.get("headline", "")
        )

        text_parts.append(
            profile.get("summary", "")
        )

        for job in career:

            text_parts.append(
                job.get("title", "")
            )

            text_parts.append(
                job.get("description", "")
            )

        for skill in skills:

            text_parts.append(
                skill.get("name", "")
            )

        full_text = " ".join(
            text_parts
        ).lower()

        retrieval_fit = self._keyword_score(
            full_text,
            self.RETRIEVAL_TERMS
        )

        evaluation_fit = self._keyword_score(
            full_text,
            self.EVALUATION_TERMS
        )

        product_fit = self._product_company_score(
            career
        )

        ai_company_fit = self._ai_company_score(
            career
        )

        behavior_fit = self._behavior_score(
            signals
        )

        availability_fit = self._availability_score(
            signals
        )

        trust_score = self._trust_score(
            signals
        )

        return {

            "retrieval_fit":
                retrieval_fit,

            "evaluation_fit":
                evaluation_fit,

            "product_fit":
                product_fit,

            "ai_company_fit":
                ai_company_fit,

            "behavior_fit":
                behavior_fit,

            "availability_fit":
                availability_fit,

            "trust_score":
                trust_score
        }

    def _keyword_score(
        self,
        text,
        keywords
    ):

        matches = sum(
            1
            for kw in keywords
            if kw in text
        )

        return min(
            matches / 5,
            1.0
        )

    def _product_company_score(
        self,
        career
    ):

        score = 0

        for job in career:

            company = (
                job.get(
                    "company",
                    ""
                )
                .lower()
            )

            if company in self.PRODUCT_COMPANIES:
                score += 1

        return min(
            score / 3,
            1.0
        )

    def _ai_company_score(
        self,
        career
    ):

        score = 0

        for job in career:

            company = (
                job.get(
                    "company",
                    ""
                )
                .lower()
            )

            if company in self.AI_COMPANIES:
                score += 1

        return min(
            score,
            1.0
        )

    def _behavior_score(
        self,
        signals
    ):

        response_rate = signals.get(
            "recruiter_response_rate",
            0
        )

        interview_completion = signals.get(
            "interview_completion_rate",
            0
        )

        saved = min(
            signals.get(
                "saved_by_recruiters_30d",
                0
            ) / 20,
            1.0
        )

        return round(
            (
                response_rate * 0.4
                + interview_completion * 0.4
                + saved * 0.2
            ),
            3
        )

    def _availability_score(
        self,
        signals
    ):

        score = 0

        if signals.get(
            "open_to_work_flag",
            False
        ):
            score += 0.5

        notice = signals.get(
            "notice_period_days",
            180
        )

        if notice <= 30:
            score += 0.5

        elif notice <= 60:
            score += 0.3

        elif notice <= 90:
            score += 0.1

        return round(
            min(score, 1.0),
            3
        )

    def _trust_score(
        self,
        signals
    ):

        score = 0

        if signals.get(
            "verified_email",
            False
        ):
            score += 0.4

        if signals.get(
            "verified_phone",
            False
        ):
            score += 0.4

        if signals.get(
            "linkedin_connected",
            False
        ):
            score += 0.2

        return round(
            score,
            3
        )