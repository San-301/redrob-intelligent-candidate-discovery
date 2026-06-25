# src/utils/submission_generator.py

import pandas as pd


class SubmissionGenerator:

    def generate_csv(
        self,
        ranked_candidates,
        output_path
    ):

        rows = []

        for rank, candidate in enumerate(
            ranked_candidates[:100],
            start=1
        ):

            rows.append({
                "candidate_id": candidate["candidate_id"],
                "rank": rank,
                "score": candidate["score"],
                "reasoning": candidate["reasoning"]
            })
            

        df = pd.DataFrame(rows)

        df.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        print(
            f"Submission saved to: "
            f"{output_path}"
        )

        return df