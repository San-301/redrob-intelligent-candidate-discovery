import os
import faiss
import numpy as np


class FAISSIndex:

    def __init__(
        self,
        embedding_dim: int = 384,
        index_path: str = "models/faiss_candidates.index"
    ):

        self.embedding_dim = embedding_dim
        self.index_path = index_path

        # Cosine similarity
        self.index = faiss.IndexHNSWFlat(
            embedding_dim,
            32,
            faiss.METRIC_INNER_PRODUCT    
            
        )

        self.index.hnsw.efConstruction = 200
        self.index.hnsw.efSearch = 64

        self.candidate_ids = []

    def build_index(
        self,
        embeddings,
        candidate_ids
    ):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        faiss.normalize_L2(
            embeddings
        )

        self.index = faiss.IndexHNSWFlat(
            self.embedding_dim,
            32,
            faiss.METRIC_INNER_PRODUCT
        )

        self.index.hnsw.efConstruction = 200
        self.index.hnsw.efSearch = 64

        self.index.add(
            embeddings
        )

        self.candidate_ids = list(
            candidate_ids
        )

        print(
            f"FAISS index built with {self.index.ntotal} candidates"
        )

    def search(
        self,
        query_embedding,
        top_k=100
    ):

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(
            query_embedding
        )

        top_k = min(top_k, self.index.ntotal)

        scores, indices = (
            self.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx < 0:
                continue

            results.append({

                "candidate_id":
                    self.candidate_ids[idx],

                "semantic_score":
                     max(
                    0.0,
                    min(float(score), 1.0)
                )
            })

        return results

    def save(self):

        os.makedirs(
            os.path.dirname(
                self.index_path
            ),
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            self.index_path
        )

        np.save(
            self.index_path + "_ids.npy",
            np.array(
                self.candidate_ids
            )
        )

        print(
            f"Saved FAISS index "
            f"to {self.index_path}"
        )

    def load(self):

        self.index = (
            faiss.read_index(
                self.index_path
            )
        )

        self.candidate_ids = (
            np.load(
                self.index_path +
                "_ids.npy",
                allow_pickle=True
            ).tolist()
        )

        print(
            f"Loaded FAISS index "
            f"with {len(self.candidate_ids)} candidates"
        )

    def size(self):

        return self.index.ntotal