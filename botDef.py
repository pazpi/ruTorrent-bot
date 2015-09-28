# botDef.py
#import logging
import telegram
import config

startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /start \n- \n- /help \n- /magnet \n- /host"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/magnet - Add torrent with magnetic link \n/help - This message will be shown \n/info - Show more info about me \n\nFor Example: \n/magnet magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce"


#module_logger = logging.getLogger(__name__)

bot = telegram.Bot(config.TOKEN)
text = ''
chat_id = '' # unique id for the chat user - for now the bot will be able to serve one person at a time
update_id = '' 
#LAST_UPDATE_ID = ''
LAST_UPDATE_ID = bot.getUpdates()[-1].update_id

# def __init__(self):
    # self.logger = logging.getLogger("telegram_bot.Bot")
    # self.logger.info("Bot creation")


def update():
    updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    for update in updates:
        text = update.message.text
        chat_id = update.message.chat.id
        update_id = update.update_id


def firstConfig(self):
    self.sendMsg(startTxt)
    self.sendMsg("Tell me the host address \n Es: http://myaddress.me")
    update()
    address = fetchLastMsg()
    self.sendMsg("Tell me the host port \n Es: 8080")
    port = fetchLastMsg()
    self.sendMsg("Tell me the host username")
    username = fetchLastMsg()
    self.sendMsg("Tell me the host password")
    password = fetchLastMsg()
    rispCorrec = "Correct? \nAddress: " + address + "\nPort: "+ port + "\nUsername: "+ username + "\nPassword: "+ password
    self.sendMsg(rispCorrec)
    #to implement the database to save all datas. for now we can put info in the config.py file
    # Non funziona, non salva le variabili su file
    # config.ADDRESS = address
    # config.PORT = port
    # config.USERNAME = username
    # config.PASSWORD = password

def helpMessage(self):
    self.sendMsg(helpTxt)

def infoMessage(self):
    self.sendMsg(infoTxt)

def sendMsg(self, text):
    self.bot.sendMessage(chat_id=self.chat_id, text=text)

def setKeyboard(*args):
    for arg in args:
        keyboard.append(arg)
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    self.bot.sendMessage(chat_id=self.chat_id, text="Choose wisely", reply_markup=reply_markup)
