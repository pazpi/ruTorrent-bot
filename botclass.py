# telegram_bot.py
import logging
import telegram
import config

startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /start \n- \n- /help \n- /magnet \n- /host"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/magnet - Add torrent with magnetic link \n/help - This message will be shown \n/info - Show more info about me \n\nFor Example: \n/magnet magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce"


module_logger = logging.getLogger(__name__)

class Bot:
    bot = telegram.Bot(config.TOKEN)
    text = ''
    chat_id = ''
    update_id = ''
    LAST_UPDATE_ID = ''
    def __init__(self):
        self.logger = logging.getLogger("telegram_bot.Bot")
        self.logger.info("Bot creation")
        self.LAST_UPDATE_ID = self.bot.getUpdates()[-1].update_id

    def update(self):
        updates = self.bot.getUpdates(offset=self.LAST_UPDATE_ID)
        for update in updates:
            self.text = update.message.text
            self.chat_id = update.message.chat.id
            self.update_id = update.update_id

    def lastMessage(self):
        self.update()
        message = self.text
        return message

    def firstConfig(self):
        self.sendMessage(chat_id=self.chat_id, text=startTxt)
        self.sendMessage(chat_id=self.chat_id, text="Tell me the host address \n Es: http://myaddress.me")
        address = lastMessage()
        self.sendMessage(chat_id=self.chat_id, text="Tell me the host port \n Es: 8080")
        port = lastMessage()
        self.sendMessage(chat_id=self.chat_id, text="Tell me the host username")
        username = lastMessage()
        self.sendMessage(chat_id=self.chat_id, text="Tell me the host password")
        password = lastMessage()
        rispCorrec = "Correct? \nAddress: " + address + "\nPort: "+ port + "\nUsername: "+ username + "\nPassword: "+ password
        self.sendMessage(chat_id=self.chat_id, text=rispCorrec)
        #to implement the database to save all datas
