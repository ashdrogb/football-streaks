from dataclasses import dataclass


@dataclass
class Match:

    date: str
    league: str

    home_team: str
    away_team: str

    home_team_id: int
    away_team_id: int

    home_crest: str
    away_crest: str

    home_score: int
    away_score: int