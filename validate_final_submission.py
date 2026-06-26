import pandas as pd
import json
import sys
from pathlib import Path


def load_candidate_ids(candidate_file):

    ids = set()

    with open(
        candidate_file,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            if line.strip():

                obj = json.loads(line)

                ids.add(
                    obj["candidate_id"]
                )

    return ids


def validate(
    submission_path,
    candidate_path
):

    print("\n========== FINAL VALIDATION ==========\n")

    errors = []
    warnings = []

    # --------------------------------------------------
    # File exists
    # --------------------------------------------------

    if not Path(submission_path).exists():

        print("❌ Submission file not found")
        return

    df = pd.read_csv(submission_path)

    # --------------------------------------------------
    # Required columns
    # --------------------------------------------------

    required_cols = [
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ]

    if list(df.columns) != required_cols:

        errors.append(
            f"Columns must be exactly: {required_cols}"
        )

    # --------------------------------------------------
    # Row count
    # --------------------------------------------------

    if len(df) != 100:

        errors.append(
            f"Expected 100 rows, found {len(df)}"
        )

    # --------------------------------------------------
    # Unique ranks
    # --------------------------------------------------

    expected_ranks = set(range(1, 101))

    if set(df["rank"]) != expected_ranks:

        errors.append(
            "Ranks must contain 1-100 exactly once"
        )

    # --------------------------------------------------
    # Duplicate candidates
    # --------------------------------------------------

    if df["candidate_id"].duplicated().any():

        dupes = (
            df[df["candidate_id"]
            .duplicated()]
            ["candidate_id"]
            .tolist()
        )

        errors.append(
            f"Duplicate candidate IDs: {dupes}"
        )

    # --------------------------------------------------
    # Candidate IDs exist
    # --------------------------------------------------

    valid_ids = load_candidate_ids(
        candidate_path
    )

    invalid = []

    for cid in df["candidate_id"]:

        if cid not in valid_ids:

            invalid.append(cid)

    if invalid:

        errors.append(
            f"Invalid candidate IDs: {invalid}"
        )

    # --------------------------------------------------
    # Score monotonicity
    # --------------------------------------------------

    scores = df["score"].tolist()

    for i in range(len(scores) - 1):

        if scores[i] < scores[i + 1]:

            errors.append(
                f"Scores increase at rows "
                f"{i+1} -> {i+2}"
            )

            break

    # --------------------------------------------------
    # Score uniqueness
    # --------------------------------------------------

    unique_scores = df["score"].nunique()

    if unique_scores < 20:

        warnings.append(
            f"Only {unique_scores} unique scores"
        )

    # --------------------------------------------------
    # Reasoning checks
    # --------------------------------------------------

    empty_reasoning = (
        df["reasoning"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )

    if empty_reasoning > 0:

        errors.append(
            f"{empty_reasoning} empty reasonings"
        )

    unique_reasonings = (
        df["reasoning"]
        .nunique()
    )

    if unique_reasonings < 30:

        warnings.append(
            "Reasonings appear highly templated"
        )

    # --------------------------------------------------
    # Reasoning length
    # --------------------------------------------------

    avg_len = (
        df["reasoning"]
        .astype(str)
        .str.len()
        .mean()
    )

    if avg_len < 80:

        warnings.append(
            "Reasonings may be too short"
        )

    # --------------------------------------------------
    # Rank-tone consistency
    # --------------------------------------------------

    top10 = df.head(10)

    if (
        top10["reasoning"]
        .str.contains(
            "adjacent profile|notable gaps",
            case=False,
            regex=True
        )
        .any()
    ):

        warnings.append(
            "Top-10 contains negative reasoning"
        )

    bottom10 = df.tail(10)

    if (
        bottom10["reasoning"]
        .str.contains(
            "exceptional fit",
            case=False
        )
        .sum() > 3
    ):

        warnings.append(
            "Bottom candidates sound overly strong"
        )

    # --------------------------------------------------
    # Honeypot sanity
    # --------------------------------------------------

    suspicious = (
        df["reasoning"]
        .str.contains(
            "profile consistency concerns|multiple profile inconsistencies",
            case=False
        )
        .sum()
    )

    print(
        f"Candidates flagged by reasoning: "
        f"{suspicious}"
    )

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Unique Scores: {unique_scores}"
    )

    print(
        f"Unique Reasonings: {unique_reasonings}"
    )

    print(
        f"Average Reason Length: "
        f"{avg_len:.1f}"
    )

    print()

    if warnings:

        print("⚠ WARNINGS")

        for w in warnings:

            print("-", w)

        print()

    if errors:

        print("❌ VALIDATION FAILED")

        for e in errors:

            print("-", e)

    else:

        print(
            "✅ FINAL VALIDATION PASSED"
        )

        print(
            "Submission ready for upload."
        )


if __name__ == "__main__":

    if len(sys.argv) != 3:

        print(
            "Usage:\n"
            "python validate_final_submission.py "
            "submission.csv candidates.jsonl"
        )

        sys.exit()

    validate(
        sys.argv[1],
        sys.argv[2]
    )