from typing import Dict


class JDParser:

    def parse(self, jd_text: str) -> Dict:

        jd = jd_text.lower()

        return {

            # Core requirements
            "requires_retrieval":
                self._contains_any(
                    jd,
                    [
                        "retrieval",
                        "ranking",
                        "search",
                        "recommendation"
                    ]
                ),

            "requires_embeddings":
                self._contains_any(
                    jd,
                    [
                        "embeddings",
                        "vector",
                        "dense retrieval"
                    ]
                ),

            "requires_evaluation":
                self._contains_any(
                    jd,
                    [
                        "ndcg",
                        "mrr",
                        "map",
                        "evaluation"
                    ]
                ),

            "requires_llm":
                self._contains_any(
                    jd,
                    [
                        "llm",
                        "fine-tuning",
                        "lora",
                        "qlora"
                    ]
                ),

            # Experience range
            "min_exp": 5,
            "max_exp": 9,

            # Behavioral preferences
            "shipper_mindset": True,
            "product_engineering": True,

            # Penalties
            "avoid_pure_research": True,
            "avoid_keyword_stuffing": True,
            "avoid_consulting_only": True,

            # Location
            "preferred_locations": [
                "pune",
                "noida",
                "hyderabad",
                "mumbai",
                "delhi"
            ]
        }

    @staticmethod
    def _contains_any(text, keywords):

        return any(
            keyword in text
            for keyword in keywords
        )