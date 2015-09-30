# botDef.py
import logging
import telegram
import config
from asyncio.log import logger
from symbol import parameters

startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /help \n- /info \n- /hash"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/help - This message will be shown \n/info - Show more info about me \n/hash - To add a torrent from his hash\n\nTo add a Torrend from his magnet link just sent the link :D\n\n"


bot = telegram.Bot(config.TOKEN)
text = ''
chat_id = '' # unique id for the chat user - for now the bot will be able to serve one person at a time
update_id = ''
username = ''
LAST_UPDATE_ID = bot.getUpdates()[-1].update_id

chat_id_conf = {}

def __init__(self):
    logger = logging.getLogger("telegram_bot.Bot")
    logger.info("Bot creation")


def update():
    #===========================================================================
    # updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    global text
    global chat_id
    global update_id
    global username
    for update in updates:
        text = update.message.text
        chat_id = update.message.chat.id
        update_id = update.update_id
        #username = update.username


def readConfig():
    parameter = []
    global chat_id
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "r")
    for line in f:
        parameter.append(line[:-1])
    f.close()
    return parameter


def writeConfig(data,index):
    global chat_id
    parameter = []
    parameter = readConfig()
    print("parameter befor writing" + str(parameter))
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "w")
    parameter.insert(index, data + "\n")
    print("parameter after writing" + str(parameter))
    for index1 in parameter:
        f.write(index1)
    f.close()


def firstConfig():
    global chat_id
    global text
    global username
    # Add username to chat_id config dictionare, add user to still config list
    if username not in chat_id_conf:
        chat_id_conf[username] = chat_id
    answer="ciao"
    parameter = readConfig()
    if not(parameter):
        answer = "Tell me the host address \n Es: http://myaddress.me"
        writeConfig("0", 0)
    else:
        if parameter[0]=="0":
            if not text[:7] == ("http://" or "https:/"):
                  answer = "Address not correct, please follow the example. http://myaddress.me"

            writeConfig(text, 1)
            writeConfig("1", 0)
            answer = "Tell me the host port \n Es: 8080"
        if parameter[0]=="1":
            writeConfig(text, 2)
            writeConfig("2", 0)
            answer = "Tell me the host username. "
        if parameter[0]=="2":
            writeConfig(text, 3)
            writeConfig("3", 0)
            answer = "Tell me the host password"
        if parameter[0]=="3":
            writeConfig(text, 4)
            writeConfig("4", 0)
            answer = "Correct? \nAddress: " + address + "\nPort: "+ port + "\nUsername: "+ username + "\nPassword: "+ password
    return answer


# def setKeyboard(*args):
#     keyboard = []
#     for arg in args:
#         keyboard.append(arg)
#     reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
#     self.bot.sendMessage(chat_id=self.chat_id, text="Choose wisely", reply_markup=reply_markup)


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
