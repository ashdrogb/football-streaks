# scripts/refresh_data.py
"""
Fetches completed fixtures for every configured league
and writes them to the local SQLite database.

Run this before send_alerts.py to ensure streak calculations
are based on up-to-date match results.

Usage:
    python -m scripts.refresh_data
"""

from app.collectors.football_data import FootballDataCollector
from app.config.leagues import LEAGUES
from app.database.connection import get_connection


def _ensure_tables(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS matches (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT    NOT NULL,
            league      TEXT    NOT NULL,
            home_team   TEXT    NOT NULL,
            away_team   TEXT    NOT NULL,
            home_score  INTEGER NOT NULL,
            away_score  INTEGER NOT NULL,
            UNIQUE (date, home_team, away_team)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sent_alerts (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            league        TEXT    NOT NULL,
            team          TEXT    NOT NULL,
            streak_length INTEGER NOT NULL,
            sent_at       TEXT    NOT NULL
        )
        """
    )
    conn.commit()


def refresh():

    collector = FootballDataCollector()
    conn      = get_connection()

    _ensure_tables(conn)

    for league_name, league_code in LEAGUES.items():

        try:

            print(f"Fetching {league_name} …")

            matches = collector.get_completed_matches(league_code)

            rows_added = 0

            for m in matches:

                try:

                    conn.execute(
                        """
                        INSERT OR IGNORE INTO matches
                            (date, league, home_team, away_team, home_score, away_score)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            m.date,
                            m.league,
                            m.home_team,
                            m.away_team,
                            m.home_score,
                            m.away_score,
                        ),
                    )

                    rows_added += conn.execute("SELECT changes()").fetchone()[0]

                except Exception as row_err:

                    print(f"  Row error: {row_err}")

            conn.commit()

            print(f"  → {rows_added} new rows for {league_name}")

        except Exception as e:

            print(f"Failed to fetch {league_name}: {e}")

    conn.close()

    print("Refresh complete.")


if __name__ == "__main__":
    refresh()
