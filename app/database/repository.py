from datetime import datetime

from app.database.connection import (
    get_connection
)


class AlertRepository:

    @staticmethod
    def alert_exists(
        league,
        team,
        streak_length
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM sent_alerts
            WHERE league = ?
            AND team = ?
            AND streak_length = ?
            """,
            (
                league,
                team,
                streak_length
            )
        )

        exists = cursor.fetchone()

        conn.close()

        return exists is not None

    @staticmethod
    def save_alert(
        league,
        team,
        streak_length
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sent_alerts
            (
                league,
                team,
                streak_length,
                sent_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                league,
                team,
                streak_length,
                datetime.utcnow().isoformat()
            )
        )

        conn.commit()

        conn.close()