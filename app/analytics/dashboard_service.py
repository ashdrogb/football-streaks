from app.collectors.football_data import FootballDataCollector
from app.analytics.streak_scanner import StreakScanner
from app.config.leagues import LEAGUES


class DashboardService:

    @staticmethod
    def get_all_streaks():

        collector = FootballDataCollector()

        all_streaks = []

        for league_name, league_code in LEAGUES.items():

            try:

                print(f"Scanning {league_name}")

                matches = collector.get_completed_matches(
                    league_code
                )

                all_streaks.extend(
                    StreakScanner.scan(matches)
                )

            except Exception as e:

                print(
                    f"Failed {league_name}: {e}"
                )

        return all_streaks