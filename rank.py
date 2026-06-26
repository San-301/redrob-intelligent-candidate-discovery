import argparse
import json
import pandas as pd
import time
from src.ranking.ranker import CandidateRanker


def load_candidates(path):

    candidates = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            if line.strip():

                candidates.append(
                    json.loads(line)
                )

    return candidates


def get_jd_features():
    """
    Hardcoded JD features for released JD.
    Update if organizers release a new JD.
    """

    return {

        "min_exp": 3,

        "max_exp": 10,

        "must_have_skills": [
            "retrieval",
            "semantic search",
            "embeddings",
            "ranking",
            "recommendation systems",
            "llms"
        ]
    }


def create_submission(
    ranked_candidates,
    output_path
):

    rows = []

    for candidate in ranked_candidates:

        rows.append({

            "candidate_id":
                candidate["candidate_id"],

            "rank":
                candidate["rank"],

            "score":
                candidate["score"],

            "reasoning":
                candidate["reasoning"]
        })

    submission = pd.DataFrame(rows)

    submission = submission[
        [
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    ]

    submission.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

    print(
        f"Submission saved to "
        f"{output_path}"
    )

    print(
        f"Rows: {len(submission)}"
    )


def main():

    start = time.time()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--candidates",
        required=True,
        help="Path to candidates.jsonl"
    )

    parser.add_argument(
        "--out",
        default="submission.csv",
        help="Output CSV file"
    )

    args = parser.parse_args()

    print("Loading candidates...")

    candidates = load_candidates(
        args.candidates
    )

    print(
        f"Loaded {len(candidates)} candidates"
    )

    jd_features = get_jd_features()

    ranker = CandidateRanker(
        jd_features
    )

    print("Ranking candidates...")

    top_candidates = ranker.get_top_k(
        candidates,
        k=100
    )

    create_submission(
        top_candidates,
        args.out
    )

    runtime = time.time() - start

    print(
        f"Total Runtime: {runtime:.2f} seconds"
    )

    print("Done.")


if __name__ == "__main__":
    main()