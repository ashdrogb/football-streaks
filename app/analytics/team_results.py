from app.collectors.base import Match


class TeamResultsBuilder:
    """
    Derives a team's result sequence and latest match from
    a flat list of Match objects covering an entire league.
    """

    @staticmethod
    def build_results(matches: list[Match], team: str) -> list[str]:
        """
        Return a list of "W" / "D" / "L" strings for *team*,
        sorted newest-first (index 0 = most recent match).
        """
        team_matches = [
            m for m in matches
            if m.home_team == team or m.away_team == team
        ]

        # Sort descending by date string (ISO-8601 sorts lexicographically)
        team_matches.sort(key=lambda m: m.date, reverse=True)

        results = []

        for match in team_matches:
            if match.home_team == team:
                goals_for     = match.home_score
                goals_against = match.away_score
            else:
                goals_for     = match.away_score
                goals_against = match.home_score

            if goals_for > goals_against:
                results.append("W")
            elif goals_for < goals_against:
                results.append("L")
            else:
                results.append("D")

        return results

    @staticmethod
    def latest_match(matches: list[Match], team: str) -> Match:
        """
        Return the single most-recent Match involving *team*.
        Raises ValueError when the team has no matches.
        """
        team_matches = [
            m for m in matches
            if m.home_team == team or m.away_team == team
        ]

        if not team_matches:
            raise ValueError(f"No matches found for team: {team}")

        return max(team_matches, key=lambda m: m.date)
