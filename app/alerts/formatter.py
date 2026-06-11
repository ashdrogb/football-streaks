from app.analytics.models import LossStreakAlert


class AlertFormatter:

    @staticmethod
    def format(alert: LossStreakAlert):

        return (
            "🚨 SACK WATCH ALERT 🚨\n\n"
            f"League: {alert.league}\n"
            f"Team: {alert.team}\n"
            f"Current Loss Streak: {alert.loss_streak}\n"
            f"Last Opponent: {alert.last_opponent}\n"
            f"Match Date: {alert.match_date}\n"
        )