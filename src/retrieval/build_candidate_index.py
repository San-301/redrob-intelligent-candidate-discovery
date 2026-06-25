# src/retrieval/build_candidate_index.py

from src.preprocessing.load_data import CandidateDataLoader
from src.embeddings.embedding_model import EmbeddingModel
from src.retrieval.faiss_index import FAISSIndex


def build_candidate_index():

    loader = CandidateDataLoader(
        "data/raw/candidates.jsonl"
    )

    candidates = loader.load_all()

    print(
        f"Loaded {len(candidates)} candidates"
    )

    model = EmbeddingModel()

    embeddings = []
    candidate_ids = []

    for idx, candidate in enumerate(
        candidates,
        start=1
    ):

        try:

            embedding = (
                model.encode_candidate(
                    candidate
                )
            )

            embeddings.append(
                embedding
            )

            candidate_ids.append(
                candidate["candidate_id"]
            )

            if idx % 1000 == 0:

                print(
                    f"Processed {idx} candidates"
                )

        except Exception as e:

            print(
                f"Failed candidate "
                f"{candidate.get('candidate_id')}: "
                f"{e}"
            )

    index = FAISSIndex()

    index.build_index(
        embeddings,
        candidate_ids
    )

    index.save()

    print(
        "\nIndex creation complete"
    )

    print(
        f"Indexed candidates: "
        f"{index.size()}"
    )


if __name__ == "__main__":

    build_candidate_index()
