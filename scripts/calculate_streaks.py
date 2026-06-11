# scripts/calculate_streaks.py
"""
Prints all active win / draw / loss streaks across every
configured league.  Useful for a quick sanity-check without
sending Telegram alerts.

Usage:
    python -m scripts.calculate_streaks
"""

from app.analytics.global_streaks import GlobalStreakScanner


def main():

    print("Calculating streaks across all leagues …\n")

    streaks = GlobalStreakScanner.scan()

    if not streaks:
        print("No active streaks found.")
        return

    for s in streaks:
        print(
            f"[{s.league}]  {s.team:<30} "
            f"{s.streak_type.upper()} streak: {s.streak_length}  "
            f"(last vs {s.last_opponent} on {s.match_date})"
        )


if __name__ == "__main__":
    main()
