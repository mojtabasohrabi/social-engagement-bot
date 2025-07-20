import logging
from telegram import Bot
from app.core.config import settings

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self):
        self.bot = None
        if settings.TELEGRAM_BOT_TOKEN:
            try:
                self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            except Exception as e:
                logger.error(f"Failed to initialize Telegram bot: {e}")

    async def send_notification(self, chat_id: str, message: str):
        """Send notification to Telegram user"""
        if not self.bot:
            logger.warning("Telegram bot not initialized, skipping notification")
            return

        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")

    def send_notification_sync(self, chat_id: str, message: str):
        """Synchronous version for use in Celery tasks"""
        if not self.bot:
            logger.warning("Telegram bot not initialized, storing message in database")
            return False

        try:
            self.bot.send_message(chat_id=chat_id, text=message)
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False


telegram_service = TelegramService()
