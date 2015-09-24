# telegram_bot.py
import logging
import telegram
import config

module_logger = logging.getLogger(__name__)

class Bot:
    bot = telegram.Bot(config.TOKEN)
    command = ''
    chat_id = ''
    update_id = ''
    LAST_UPDATE_ID = ''
    def __init__(self):
        self.logger = logging.getLogger("telegram_bot.Bot")
        self.logger.info("Bot creation")
        self.LAST_UPDATE_ID = self.bot.getUpdates()[-1].update_id
    
    def Update(self):
        updates = self.bot.getUpdates(offset=self.LAST_UPDATE_ID)
        for update in updates:
            self.command = update.message.text
            self.chat_id = update.message.chat.id
            self.update_id = update.update_id