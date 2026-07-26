import csv
from pathlib import Path
from typing import Iterable

from analyzer.storage import DATA_FILE

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def load_observations() -> list[dict[str, str]]:
    """Load all saved observations from the research CSV."""
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def search_observations(username: str) -> list[dict[str, str]]:
    """Return observations matching a username, case-insensitively."""
    cleaned = username.strip().lstrip("@").casefold()
    return [
        row
        for row in load_observations()
        if row.get("username", "").casefold() == cleaned
    ]


def _display_rows(rows: Iterable[dict[str, str]], title: str) -> None:
    rows = list(rows)
    if not rows:
        print("\nNo matching observations found.")
        return

    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)

    for index, row in enumerate(rows, start=1):
        print(f"\nObservation #{index}")
        print(f"Timestamp: {row.get('timestamp', '')}")
        print(f"Username: @{row.get('username', '')}")
        print(f"Posts per day: {row.get('posts_per_day', '')}")
        print(f"Repeated phrases: {row.get('repeated_phrases', '')}")
        print(f"Similarity score: {row.get('similarity_score', '')}")
        print(
            "Observable Pattern Score: "
            f"{row.get('observable_pattern_score', '')}/100"
        )

    print("\n" + "=" * 62)
    print(f"Total observations shown: {len(rows)}")


def print_observations() -> None:
    _display_rows(load_observations(), "Saved Observations")


def print_search_results(username: str) -> None:
    cleaned = username.strip().lstrip("@")
    _display_rows(search_observations(cleaned), f"History for @{cleaned}")


def print_summary() -> None:
    observations = load_observations()
    if not observations:
        print("\nNo saved observations found.")
        return

    scores = [float(row["observable_pattern_score"]) for row in observations]
    usernames = {row["username"].casefold() for row in observations}

    print("\n" + "=" * 44)
    print("Research Summary")
    print("=" * 44)
    print(f"Total observations: {len(observations)}")
    print(f"Unique usernames: {len(usernames)}")
    print(f"Average pattern score: {sum(scores) / len(scores):.2f}/100")
    print(f"Lowest pattern score: {min(scores):.2f}/100")
    print(f"Highest pattern score: {max(scores):.2f}/100")
    print("=" * 44)


def export_text_report() -> Path | None:
    observations = load_observations()
    if not observations:
        return None

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / "observations_report.txt"

    scores = [float(row["observable_pattern_score"]) for row in observations]
    usernames = {row["username"].casefold() for row in observations}

    lines = [
        "Threads Agent Observatory — Research Report",
        "=" * 50,
        f"Total observations: {len(observations)}",
        f"Unique usernames: {len(usernames)}",
        f"Average pattern score: {sum(scores) / len(scores):.2f}/100",
        "",
    ]

    for index, row in enumerate(observations, start=1):
        lines.extend(
            [
                f"Observation #{index}",
                f"Timestamp: {row['timestamp']}",
                f"Username: @{row['username']}",
                f"Posts per day: {row['posts_per_day']}",
                f"Repeated phrases: {row['repeated_phrases']}",
                f"Similarity score: {row['similarity_score']}",
                f"Observable Pattern Score: {row['observable_pattern_score']}/100",
                "-" * 50,
            ]
        )

    report_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_file

