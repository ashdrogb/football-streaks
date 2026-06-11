from dataclasses import dataclass


@dataclass
class SentAlert:

    league: str
    team: str
    streak_length: int
    sent_at: str
