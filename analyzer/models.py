"""
Core data models for the Threads Agent Observatory.
"""

from dataclasses import dataclass


@dataclass
class AccountObservation:
    """
    Represents one observable account profile.
    """

    username: str
    posts_per_day: float
    repeated_phrases: int
    similarity_score: float
