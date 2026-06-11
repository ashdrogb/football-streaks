# app/alerts/telegram.py

import requests

from app.config.settings import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)


class TelegramAlertSender:

    @staticmethod
    def send(message: str):

        if not TELEGRAM_TOKEN:
            raise ValueError(
                "TELEGRAM_TOKEN not configured"
            )

        if not TELEGRAM_CHAT_ID:
            raise ValueError(
                "TELEGRAM_CHAT_ID not configured"
            )

        url = (
            f"https://api.telegram.org/bot"
            f"{TELEGRAM_TOKEN}/sendMessage"
        )

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }

        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()