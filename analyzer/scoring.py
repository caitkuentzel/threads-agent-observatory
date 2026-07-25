"""
Scoring engine.
"""

from analyzer.models import AccountObservation


def calculate_score(account: AccountObservation) -> float:
    """
    Calculates an observable-pattern score.

    This is NOT a bot score.
    It simply measures observable characteristics.
    """

    posting = min(account.posts_per_day / 50, 1.0) * 25
    repetition = min(account.repeated_phrases / 10, 1.0) * 30
    similarity = max(0.0, min(account.similarity_score, 1.0)) * 45

    total = posting + repetition + similarity

    return round(total, 2)
