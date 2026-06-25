import json
from pathlib import Path
from typing import Generator, Dict, List

import pandas as pd


class CandidateDataLoader:
    """
    Loads Redrob candidate dataset efficiently.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.file_path}"
            )

    def load_jsonl(self) -> Generator[Dict, None, None]:
        """
        Stream candidates one-by-one.
        Best option for 100k records.
        """

        with open(self.file_path, "r", encoding="utf-8") as f:

            for line_num, line in enumerate(f, start=1):

                line = line.strip()

                if not line:
                    continue

                try:
                    yield json.loads(line)

                except json.JSONDecodeError as e:
                    print(
                        f"[WARNING] Skipping invalid JSON "
                        f"at line {line_num}: {e}"
                    )

    def load_n_records(self, n: int = 100) -> List[Dict]:
        """
        Load first N candidates.
        Useful for testing.
        """

        records = []

        for i, candidate in enumerate(self.load_jsonl()):

            records.append(candidate)

            if i + 1 >= n:
                break

        return records

    def load_all(self) -> List[Dict]:
        """
        Load entire dataset.
        Use only if RAM allows.
        """

        return list(self.load_jsonl())

    def to_dataframe(self, n: int = None) -> pd.DataFrame:
        """
        Convert candidates to DataFrame.
        Useful for EDA/debugging.
        """

        if n:
            data = self.load_n_records(n)
        else:
            data = self.load_all()

        return pd.json_normalize(data)


if __name__ == "__main__":

    loader = CandidateDataLoader(
        "data/raw/candidates.jsonl"
    )

    sample = loader.load_n_records(3)

    print(f"Loaded {len(sample)} candidates")

    print(sample[0]["candidate_id"])
    print(sample[0]["profile"]["current_title"])