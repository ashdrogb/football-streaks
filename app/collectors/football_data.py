import requests

from app.config.settings import API_KEY
from app.collectors.base import Match


class FootballDataCollector:

    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):

        self.headers = {
            "X-Auth-Token": API_KEY
        }

    def get_matches(self, competition_code):

        url = (
            f"{self.BASE_URL}/competitions/"
            f"{competition_code}/matches"
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
    
    def get_completed_matches(self, competition_code: str):

        data = self.get_matches(competition_code)

        league_name = data["competition"]["name"]

        matches = []

        for match in data["matches"]:

            if match["status"] != "FINISHED":
                continue

            matches.append(
                        Match(
                            date=match["utcDate"],
                            league=data["competition"]["name"],

                            home_team=match["homeTeam"]["name"],
                            away_team=match["awayTeam"]["name"],

                            home_team_id=match["homeTeam"]["id"],
                            away_team_id=match["awayTeam"]["id"],

                            home_crest=match["homeTeam"]["crest"],
                            away_crest=match["awayTeam"]["crest"],

                            home_score=match["score"]["fullTime"]["home"],
                            away_score=match["score"]["fullTime"]["away"]
                        )
                    )

        return matches