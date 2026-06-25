# src/retrieval/semantic_retriever.py

from src.embeddings.embedding_model import EmbeddingModel
from src.retrieval.faiss_index import FAISSIndex


class SemanticRetriever:

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        faiss_index: FAISSIndex
    ):

        self.embedding_model = embedding_model
        self.faiss_index = faiss_index

    def retrieve(
        self,
        jd_text: str,
        top_k: int = 500
    ):

        query_embedding = (
            self.embedding_model.encode_jd(
                jd_text
            )
        )

        results = (
            self.faiss_index.search(
                query_embedding,
                top_k=top_k
            )
        )

        return results