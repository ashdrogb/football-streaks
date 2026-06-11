class StreakEngine:
    """
    Computes streak statistics from a chronologically-ordered
    list of result strings (e.g. ["L", "L", "W", "D"]).

    Convention: index 0 is the most recent match.
    """

    @staticmethod
    def current_loss_streak(results: list[str]) -> int:
        """Count consecutive losses from the most recent match."""
        streak = 0
        for result in results:
            if result == "L":
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def current_win_streak(results: list[str]) -> int:
        """Count consecutive wins from the most recent match."""
        streak = 0
        for result in results:
            if result == "W":
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def current_draw_streak(results: list[str]) -> int:
        """Count consecutive draws from the most recent match."""
        streak = 0
        for result in results:
            if result == "D":
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def current_unbeaten_streak(results: list[str]) -> int:
        """Count consecutive non-loss matches (W or D)."""
        streak = 0
        for result in results:
            if result in ("W", "D"):
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def current_winless_streak(results: list[str]) -> int:
        """Count consecutive non-win matches (L or D)."""
        streak = 0
        for result in results:
            if result in ("L", "D"):
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def current_streak_type(results: list[str]) -> tuple[str, int]:
        """
        Returns the active streak type and its length.
        Returns ("none", 0) when the results list is empty.
        """
        if not results:
            return ("none", 0)

        latest = results[0]

        if latest == "W":
            return ("win", StreakEngine.current_win_streak(results))
        elif latest == "L":
            return ("loss", StreakEngine.current_loss_streak(results))
        else:
            return ("draw", StreakEngine.current_draw_streak(results))
