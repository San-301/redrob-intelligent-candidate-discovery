from src.retrieval.semantic_retriever import SemanticRetriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.ranking.ranker import CandidateRanker
from src.reasoning.skill_matcher import SkillMatcher


class RetrieveAndRank:

    def __init__(
        self,
        jd_features,
        semantic_retriever
    ):

        self.semantic_retriever = (
            semantic_retriever
        )

        self.candidate_ranker = (
            CandidateRanker(
                jd_features
            )
        )

        self.hybrid_retriever = (
            HybridRetriever(
                self.semantic_retriever,
                self.candidate_ranker
            )
        )

        self.skill_matcher = SkillMatcher()

    def search(
        self,
        jd_text,
        candidates,
        top_k_semantic=2000,
        final_k=100
    ):

        results = (
            self.hybrid_retriever
            .retrieve_and_rank(
                jd_text=jd_text,
                candidates=candidates,
                top_k_semantic=top_k_semantic,
                final_k=final_k
            )
        )

        if not results:
            return []

        for candidate in results:

            skill_result = (
                self.skill_matcher.match(
                    candidate["candidate_data"],
                    jd_text
                )
            )

            candidate["matched_skills"] = (
                skill_result["matched_skills"]
            )

            candidate["missing_skills"] = (
                skill_result["missing_skills"]
            )

        # Deterministic sorting
        results = sorted(
            results,
            key=lambda x: (
                -x["hybrid_score"],
                x["candidate_id"]
            )
        )

        return results[:final_k]
