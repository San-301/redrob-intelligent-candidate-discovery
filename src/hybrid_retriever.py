from src.ranking.ranker import CandidateRanker
from src.retrieval.semantic_retriever import SemanticRetriever


class HybridRetriever:

    def __init__(
        self,
        semantic_retriever: SemanticRetriever,
        candidate_ranker: CandidateRanker
    ):

        self.semantic_retriever = semantic_retriever
        self.candidate_ranker = candidate_ranker

    def retrieve_and_rank(
        self,
        jd_text,
        candidates,
        top_k_semantic=2000,
        final_k=100
    ):

        semantic_results = (
            self.semantic_retriever.retrieve(
                jd_text,
                top_k=top_k_semantic
            )
        )

        semantic_map = {

            item["candidate_id"]:
            item["semantic_score"]

            for item in semantic_results
        }

        shortlisted_candidates = [

            c

            for c in candidates

            if c["candidate_id"]
            in semantic_map
        ]

        ranked = (
            self.candidate_ranker
            .rank_candidates(
                shortlisted_candidates
            )
        )

        for candidate in ranked:

            semantic_score = semantic_map.get(
                candidate["candidate_id"],
                0
            )

            rule_score = candidate["score"]

            candidate[
                "semantic_score"
            ] = semantic_score

            # heavily trust rule engine for weak profiles

            if rule_score < 0.40:

                hybrid_score = (
                    0.90 * rule_score +
                    0.10 * semantic_score
                )

            # rescue hidden gems

            elif semantic_score > 0.85:

                hybrid_score = (
                    0.70 * rule_score +
                    0.30 * semantic_score
                )

            else:

                hybrid_score = (
                    0.80 * rule_score +
                    0.20 * semantic_score
                )

            # suspicious title

            if candidate["title_score"] == 0:
                hybrid_score *= 0.80

            candidate["hybrid_score"] = hybrid_score

        ranked.sort(
            key=lambda x:
            x["hybrid_score"],
            reverse=True
        )

        return ranked[:final_k]