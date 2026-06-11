from app.collectors.football_data import (
    FootballDataCollector
)

from app.analytics.streak_scanner import (
    StreakScanner
)

from app.config.leagues import LEAGUES


class GlobalStreakScanner:

    @staticmethod
    def scan():

        collector = FootballDataCollector()

        all_streaks = []

        for league_name, code in LEAGUES.items():

            try:

                print(f"Scanning {league_name}")

                matches = (
                    collector.get_completed_matches(
                        code
                    )
                )

                all_streaks.extend(
                    StreakScanner.scan(matches)
                )

            except Exception as e:

                print(
                    f"Failed to scan {league_name}: {e}"
                )

        return all_streaks