import telegram
import config.TOKEN as token

# def BotDef():
#     bot = telegram.Bot(token)
#     LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
#     
#     updates = bot.getUpdates(offset=LAST_UPDATE_ID)
#     if(not updates):
#         logger.error("Couldn't get updates")
#         return
#     for update in updates:
#         command = update.message.text
#         chat_id = update.message.chat.id
#         update_id = update.update_id
#         answer = ''
#         init.config_start(chat_id)
        
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
