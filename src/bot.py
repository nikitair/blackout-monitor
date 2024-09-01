import os
from dotenv import load_dotenv
import requests
from logging_config import logger

load_dotenv()


class TelegramBot:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
    URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    
    
    def send_message(self, message):
        response = requests.post(
            url=self.URL,
            json={
                "chat_id": self.CHANNEL_ID,
                "text": message,
                "parse_mode": "HTML"
            }    
        )
        status_code = response.status_code
        logger.info(f"telegram api status code - ({status_code})")
        logger.info(f"telegram response data - ({response.text})")


if __name__ == "__main__":
    bot = TelegramBot()
    bot.send_message("Test API")
    
    