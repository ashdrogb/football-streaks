from app.analytics.team_results import TeamResultsBuilder
from app.analytics.streak_engine import StreakEngine
from app.analytics.models import LossStreakAlert


class LeagueScanner:

    @staticmethod
    def find_loss_streaks(matches, threshold=5):
        
        teams = set()

        for match in matches:

            teams.add(match.home_team)
            teams.add(match.away_team)

        alerts = []

        league = matches[0].league if matches else "Unknown"

        for team in teams:
            
            latest_match = TeamResultsBuilder.latest_match(matches, team)

            if latest_match.home_team == team:
                opponent = latest_match.away_team
            else:
                opponent = latest_match.home_team

            results = TeamResultsBuilder.build_results(
                matches,
                team
            )

            loss_streak = StreakEngine.current_loss_streak(
                results
            )

            if loss_streak >= threshold:

                alerts.append(
                        LossStreakAlert(
                            league=league,
                            team=team,
                            loss_streak=loss_streak,
                            last_result=results[0],
                            last_opponent=opponent,
                            match_date=latest_match.date,
                            alert_triggered=True
                        )
                    )

        return alerts