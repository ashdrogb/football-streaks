import requests

from app.collectors.base import Match
from app.config.settings import API_KEY


class APIFootballCollector:

    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(self):

        self.headers = {
            "x-apisports-key": API_KEY
        }

    def get_fixtures(
        self,
        league_id: int,
        season: int
    ):

        url = f"{self.BASE_URL}/fixtures"

        params = {
            "league": league_id,
            "season": season
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()