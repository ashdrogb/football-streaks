from dataclasses import dataclass

@dataclass
class SentAlert:

    league: str
    team: str
    streak_length: int
    sent_at: str
    
@dataclass
class TeamStreak:

    league: str

    team: str
    team_id: int
    crest_url: str

    streak_type: str
    streak_length: int

    last_opponent: str
    last_opponent_crest: str

    match_date: str