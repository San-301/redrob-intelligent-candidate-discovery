import re

class SkillMatcher:
    SYNONYMS = {

                "llms": [

                    "large language model",

                    "gpt",

                    "transformer"

                ],

                "llms": [
                    "large language model",
                    "large language models",
                    "gpt",
                    "transformer",
                    "transformers"
                ],

                "rag": [

                    "retrieval augmented generation"

                ],

                "vector search": [

                    "semantic search"

                ]
            }

    def extract_jd_skills(
        self,
        jd_text
    ):

        jd_text = jd_text.lower()

        skills = [
            "rag",
            "llm",
            "llms",
            "embeddings",
            "vector search",
            "semantic search",
            "retrieval",
            "information retrieval",
            "ranking",
            "reranking",
            "re-ranking",
            "recommendation systems",
            "faiss",
            "pinecone",
            "qdrant",
            "weaviate",
            "milvus",
            "langchain",
            "bm25",
            "elasticsearch",
            "opensearch",
            "machine learning",
            "deep learning",
            "nlp",
            "tensorflow",
            "pytorch",
            "mlops"
        ]

        
        jd_skills = []

        for skill in skills:

            pattern = rf"\b{re.escape(skill)}\b"

            if re.search(
                pattern,
                jd_text
            ):
                jd_skills.append(skill)

        return list(set(jd_skills))

    def get_candidate_text(
        self,
        candidate
    ):

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

        skill_text = " ".join(
            [
                s.get(
                    "name",
                    ""
                )
                for s in skills
            ]
        )

        career_text = " ".join(
            [
                j.get(
                    "description",
                    ""
                )
                for j in career
            ]
        )

        return (
            profile.get(
                "current_title",
                ""
            )
            + " "
            + profile.get(
                "headline",
                ""
            )
            + " "
            + profile.get(
                "summary",
                ""
            )
            + " "
            + skill_text
            + " "
            + career_text
        ).lower()

    def match(
        self,
        candidate,
        jd_text
    ):

        jd_skills = self.extract_jd_skills(
            jd_text
        )

        candidate_text = (
            self.get_candidate_text(
                candidate
            )
        )

        matched = []
        missing = []

        for skill in jd_skills:

            pattern = rf"\b{re.escape(skill)}\b"

            terms = [skill]

            terms.extend(

                self.SYNONYMS.get(
                    skill,
                    []
                )
            )

            found = False

            for term in terms:

                pattern = (
                    rf"\b{re.escape(term)}\b"
                )

                if re.search(
                    pattern,
                    candidate_text
                ):

                    found = True

                    break

            if found:

                matched.append(skill)

            else:

                missing.append(skill)
        return {
            "matched_skills": matched,
            "missing_skills": missing
        }
