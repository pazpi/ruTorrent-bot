# botDef.py
#import logging
import telegram
import config
from asyncio.log import logger

startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /start \n- \n- /help \n- /magnet \n- /host"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/help - This message will be shown \n/info - Show more info about me \n/hash - To add a torrent from his hash\n\nTo add a Torrend from his magnet link just sent the link :D\n\n"


#module_logger = logging.getLogger(__name__)

bot = telegram.Bot(config.TOKEN)
text = ''
chat_id = '' # unique id for the chat user - for now the bot will be able to serve one person at a time
update_id = ''
LAST_UPDATE_ID = bot.getUpdates()[-1].update_id

# def __init__(self):
    # self.logger = logging.getLogger("telegram_bot.Bot")
    # self.logger.info("Bot creation")


def update():
    updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    global text
    global chat_id
    global update_id
    for update in updates:
        text = update.message.text
        chat_id = update.message.chat.id
        update_id = update.update_id


def readConfig():
    parameter = []
    global chat_id
    f = open("chat_id_file/" + chat_id, "r")
    for line in f:
        parameter.append(line)
    f.close()
    return parameter


def writeConfig(data,index):
    global chat_id
    parameter = readConfig()
    f = open("chat_id_file/" + chat_id, "w")
    paramete[index] = data + "\n"
    f.write(parameter)
    f.close()


# def firstConfig():
#     global chat_id
#     #bot.sendMessage(chat_id=chat_id, text=startTxt)
#     # put 0 in the first line of the chat_id.txt file
#     bot.sendMessage(chat_id=chat_id, text="Tell me the host address \n Es: http://myaddress.me")
#     #logger.debug("firstConfig")
#     bot.sendMessage(chat_id=chat_id, text="Tell me the host port \n Es: 8080")
#
#     bot.sendMessage(chat_id=chat_id, text="Tell me the host username. ")
#
#     bot.sendMessage(chat_id=chat_id, text="Tell me the host password")
#
#     rispCorrec = "Correct? \nAddress: " + address + "\nPort: "+ port + "\nUsername: "+ username + "\nPassword: "+ password
#     bot.sendMessage(chat_id=chat_id, text=rispCorrec)


# def setKeyboard(*args):
#     keyboard = []
#     for arg in args:
#         keyboard.append(arg)
#     reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
#     self.bot.sendMessage(chat_id=self.chat_id, text="Choose wisely", reply_markup=reply_markup)
#
#
# def config(chat_id):
#     # keyboard_host_port = [[ "HOST", "PORT", "EXIT"]]
#     # reply_markup = telegram.ReplyKeyboardMarkup(keyboard_host_port)
#     # bot.sendMessage(chat_id=chat_id, text="Choose wisely", reply_markup=reply_markup)
#     setKeyboard("HOST", "PORT", "EXIT")
#     if (bot.getUpdates(offset=LAST_UPDATE_ID).message.text == "HOST"):
#         setHost()
#     elif (bot.getUpdates(offset=LAST_UPDATE_ID).message.text == "PORT"):
#         setPort()
#     elif (bot.getUpdates(offset=LAST_UPDATE_ID).message.text == "EXIT"):
#         return
#     else:
#         return
