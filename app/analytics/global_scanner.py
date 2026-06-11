from app.collectors.football_data import FootballDataCollector
from app.analytics.league_scanner import LeagueScanner
from app.config.leagues import LEAGUES


class GlobalScanner:

    @staticmethod
    def scan_all_leagues(threshold=5):

        collector = FootballDataCollector()

        alerts = []

        for league_name, league_code in LEAGUES.items():
            
            try:

                print(f"Scanning {league_name}")

                matches = collector.get_completed_matches(
                    league_code
                )

                alerts.extend(
                    LeagueScanner.find_loss_streaks(
                        matches,
                        threshold
                    )
                )

            except Exception as e:

                print(
                    f"Failed to scan {league_name}: {e}"
                )

        return alerts