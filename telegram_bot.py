import telegram
import config

        
class Bot:
    bot = telegram.Bot("116051020:AAHrxECX7pDpDuQgTMYbamGVKLQCPxpVkKA")
    command = ''
    chat_id = ''
    update_id = ''
    LAST_UPDATE_ID = '' 
    def __init__(self):
        self.LAST_UPDATE_ID = self.bot.getUpdates()[-1].update_id
        updates = self.bot.getUpdates(offset=self.LAST_UPDATE_ID)
        for update in updates:
            self.command = update.message.text
            self.chat_id = update.message.chat.id
            self.update_id = update.update_id
