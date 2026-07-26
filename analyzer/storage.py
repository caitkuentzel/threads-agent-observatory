import csv
from datetime import datetime
from pathlib import Path

from analyzer.models import AccountObservation


DATA_FILE = Path("data/research_data.csv")


def save_observation(
    account: AccountObservation,
    score: float,
) -> Path:
    """Append one completed observation to the research CSV file."""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = DATA_FILE.exists()

    with DATA_FILE.open(
        mode="a",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "username",
                    "posts_per_day",
                    "repeated_phrases",
                    "similarity_score",
                    "observable_pattern_score",
                ]
            )

        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                account.username,
                account.posts_per_day,
                account.repeated_phrases,
                account.similarity_score,
                score,
            ]
        )

    return DATA_FILE
