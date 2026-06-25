# src/embeddings/semantic_ranker.py

from typing import Dict, List
import numpy as np

from src.embeddings.embedding_model import (
    EmbeddingModel
)


class SemanticRanker:

    def __init__(self):

        self.embedding_model = (
            EmbeddingModel()
        )

    @staticmethod
    def cosine_similarity(
        vector_a,
        vector_b
    ) -> float:

        similarity = np.dot(
            vector_a,
            vector_b
        )

        return float(similarity)

    def score_candidate(
        self,
        candidate: Dict,
        jd_text: str
    ) -> float:

        candidate_embedding = (
            self.embedding_model
            .encode_candidate(
                candidate
            )
        )

        jd_embedding = (
            self.embedding_model
            .encode_jd(
                jd_text
            )
        )

        similarity = (
            self.cosine_similarity(
                candidate_embedding,
                jd_embedding
            )
        )

        return round(
            similarity,
            4
        )

    def score_candidates(
        self,
        candidates: List[Dict],
        jd_text: str
    ) -> List[Dict]:

        jd_embedding = (
            self.embedding_model
            .encode_jd(
                jd_text
            )
        )

        results = []

        for candidate in candidates:

            candidate_embedding = (
                self.embedding_model
                .encode_candidate(
                    candidate
                )
            )

            similarity = (
                self.cosine_similarity(
                    candidate_embedding,
                    jd_embedding
                )
            )

            results.append(
                {
                    "candidate_id":
                        candidate[
                            "candidate_id"
                        ],

                    "semantic_score":
                        round(
                            similarity,
                            4
                        )
                }
            )

        return sorted(
            results,
            key=lambda x:
                x["semantic_score"],
            reverse=True
        )
