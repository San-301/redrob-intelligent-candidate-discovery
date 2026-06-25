# src/ranking/hybrid_ranker.py

from typing import Dict, List


class HybridRanker:

    def __init__(
        self,
        rule_weight: float = 0.80,
        semantic_weight: float = 0.20
    ):

        self.rule_weight = (
            rule_weight
        )

        self.semantic_weight = (
            semantic_weight
        )

    def combine_scores(
        self,
        rule_score: float,
        semantic_score: float
    ) -> float:

        final_score = (
            rule_score
            * self.rule_weight
            +
            semantic_score
            * self.semantic_weight
        )

        return round(
            min(
                max(
                    final_score,
                    0.0
                ),
                1.0
            ),
            4
        )

    def rank_candidates(
        self,
        rule_results: List[Dict],
        semantic_results: List[Dict]
    ) -> List[Dict]:

        semantic_map = {
            row["candidate_id"]:
            row["semantic_score"]
            for row in semantic_results
        }

        ranked = []

        for row in rule_results:

            candidate_id = (
                row["candidate_id"]
            )

            rule_score = (
                row["score"]
            )

            semantic_score = (
                semantic_map.get(
                    candidate_id,
                    0.0
                )
            )
            
            if rule_score < 0.40:
                hybrid_score = (
                    rule_score * 0.90 +
                    semantic_score * 0.10
                )

            elif semantic_score > 0.85:
                hybrid_score = (
                    rule_score * 0.70 +
                    semantic_score * 0.30
                )

            else:
                hybrid_score = self.combine_scores(
                    rule_score,
                    semantic_score
                )
                
            if row.get("title_score", 0) == 0:
                semantic_score *= 0.4

            hybrid_score = (
                self.combine_scores(
                    rule_score,
                    semantic_score
                )
            )

            result = row.copy()

            result[
                "rule_score"
            ] = rule_score

            result[
                "semantic_score"
            ] = semantic_score

            result[
                "score"
            ] = hybrid_score

            ranked.append(
                result
            )

        ranked.sort(
            key=lambda x:
                x["score"],
            reverse=True
        )

        return ranked