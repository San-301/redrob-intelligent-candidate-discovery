from sentence_transformers import SentenceTransformer
from typing import Dict, List


class EmbeddingModel:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(
            model_name
        )

    def build_candidate_text(
        self,
        candidate: Dict
    ) -> str:

        profile = candidate.get(
            "profile",
            {}
        )

        skills = candidate.get(
            "skills",
            []
        )

        career = candidate.get(
            "career_history",
            []
        )

        title = profile.get(
            "current_title",
            ""
        )

        headline = profile.get(
            "headline",
            ""
        )

        summary = profile.get(
            "summary",
            ""
        )

        skill_text = " ".join(
            [
                s.get("name", "")
                for s in skills
            ]
        )

        experience_text = " ".join(
            [
                job.get(
                    "description",
                    ""
                )
                for job in career
            ]
        )

        candidate_text = f"""
        Title:
        {title}

        Headline:
        {headline}

        Summary:
        {summary}

        Skills:
        {skill_text}

        Experience:
        {experience_text}
        """

        return candidate_text.strip()

    def build_jd_text(
        self,
        jd_text: str
    ) -> str:

        return jd_text.strip()

    def encode_text(
        self,
        text: str
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def encode_candidate(
        self,
        candidate: Dict
    ):

        text = self.build_candidate_text(
            candidate
        )

        return self.encode_text(text)

    def encode_jd(
        self,
        jd_text: str
    ):

        return self.encode_text(
            jd_text
        )
