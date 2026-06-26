import pandas as pd

df = pd.read_csv("team_Builder_of_AI.csv")

print("\n===== DUPLICATE SCORES =====")

dup_scores = df[df.duplicated(
    subset=["score"],
    keep=False
)].sort_values("score")

if len(dup_scores) == 0:
    print("No duplicate scores found.")
else:
    print(
        dup_scores[
            ["candidate_id", "rank", "score"]
        ].to_string(index=False)
    )

print("\n===== DUPLICATE REASONINGS =====")

dup_reasonings = df[df.duplicated(
    subset=["reasoning"],
    keep=False
)]

if len(dup_reasonings) == 0:
    print("No duplicate reasonings found.")
else:
    print(
        dup_reasonings[
            ["candidate_id", "rank", "reasoning"]
        ].to_string(index=False)
    )