# scripts/send_alerts.py

from app.analytics.global_scanner import GlobalScanner
from app.alerts.formatter import AlertFormatter
from app.alerts.telegram import TelegramAlertSender
from app.database.repository import AlertRepository


alerts = GlobalScanner.scan_all_leagues()

for alert in alerts:

    already_sent = (
        AlertRepository.alert_exists(
            alert.league,
            alert.team,
            alert.loss_streak
        )
    )

    if already_sent:

        print(
            f"Skipping {alert.team}"
        )

        continue

    TelegramAlertSender.send(
        AlertFormatter.format(alert)
    )

    AlertRepository.save_alert(
        alert.league,
        alert.team,
        alert.loss_streak
    )

    print(
        f"Sent alert for {alert.team}"
    )