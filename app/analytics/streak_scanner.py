from app.collectors.base import Match
from app.analytics.models import TeamStreak
from app.analytics.team_results import TeamResultsBuilder
from app.analytics.streak_engine import StreakEngine


class StreakScanner:
    """
    Scans a list of matches from one league and returns a
    TeamStreak for every team that has an active streak of
    any type (win / draw / loss).
    """

    @staticmethod
    def scan(matches: list[Match]) -> list[TeamStreak]:

        if not matches:
            return []

        teams = {m.home_team for m in matches} | {m.away_team for m in matches}

        streaks = []

        for team in teams:

            results = TeamResultsBuilder.build_results(matches, team)

            if not results:
                continue

            streak_type, streak_length = StreakEngine.current_streak_type(results)

            if streak_length == 0:
                continue

            latest = TeamResultsBuilder.latest_match(matches, team)

            if latest.home_team == team:
                team_id        = latest.home_team_id
                crest_url      = latest.home_crest
                last_opponent  = latest.away_team
                opponent_crest = latest.away_crest
            else:
                team_id        = latest.away_team_id
                crest_url      = latest.away_crest
                last_opponent  = latest.home_team
                opponent_crest = latest.home_crest

            streaks.append(
                TeamStreak(
                    league=latest.league,
                    team=team,
                    team_id=team_id,
                    crest_url=crest_url,
                    streak_type=streak_type,
                    streak_length=streak_length,
                    last_opponent=last_opponent,
                    last_opponent_crest=opponent_crest,
                    match_date=latest.date,
                )
            )

        # Longest streaks first
        streaks.sort(key=lambda s: s.streak_length, reverse=True)

        return streaks
