# botDef.py
# telegram module for easy work with bot conf
import telegram
import config
import logging

logger = logging.getLogger(__name__)

startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /help \n- /info \n- /hash"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/help - This message will be shown \n/info - Show more info about me \n/hash - To add a torrent from his hash\n\nTo add a Torrend from his magnet link just sent the link :D\n\n"

bot = telegram.Bot(config.TOKEN)
text = ''
chat_id = '' # unique id for the chat user - for now the bot will be able to serve one person at a time
update_id = ''
username = ''
LAST_UPDATE_ID = bot.getUpdates()[-1].update_id

chat_id_config = []

def __init__(self):
    logger = logging.getLogger("telegram_bot.Bot")
    logger.info("Bot creation")


def update():
    updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    global text
    global chat_id
    global update_id
    global username
    for update in updates:
        text = update.message.text
        chat_id = update.message.chat.id
        update_id = update.update_id
        # username = update.username no attribute username in update


def readConfig():
    parameter = ["","","","","",""]
    global chat_id
    name_file = "chat_id_file/" + str(chat_id)
    # doesn't create the file
    f = open(name_file, "r")
    for i in range(6):
        parameter[i]=f.readline()[:-1]
        # print(parameter[i])
        # parameter.append(line[:-1])
    f.close()
    return parameter


def writeConfig(data,index):
    global chat_id
    parameter = []
    parameter = readConfig()
    print("parameter befor writing: ")
    print(parameter)
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "w")
    parameter.pop(index)
    parameter.insert(index, data)
    print("parameter after writing")
    print(parameter)
    f.close()
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "w")
    f.write('\n'.join(str(line) for line in parameter))
    f.close()


def firstConfig():
    global chat_id
    global text
    # global username
    # Add username to chat_id config dictionare, add user to still config list
    if chat_id not in chat_id_config:
        chat_id_config.append(chat_id)
        answer = "Tell me the host address \n Es: http://myaddress.me"
        writeConfig("0", 0)
    else:
        parameter =[]
        parameter = readConfig()
        print("par=" + str(parameter))
        print ("par 0 = " + parameter[0])
        if parameter[0] == "0":
            if not text[:7] == ("http://" or "https:/"): 
                answer = "Address not correct, please follow the example.\nEs: http://myaddress.me"
            else:
                writeConfig("1", 0)
                writeConfig(text, 1)
                answer = "Tell me the host port \n Es: 8080"
        elif parameter[0]=="1":
            writeConfig(text, 2)
            writeConfig("2", 0)
            answer = "Tell me the host username."
        elif parameter[0]=="2":
            writeConfig(text, 3)
            writeConfig("3", 0)
            answer = "Tell me the host password"
        elif parameter[0]=="3":
            writeConfig(text, 4)
            writeConfig("4", 0)
            answer = ""
            #answer = "Correct? \nAddress: " + parameter[1] + "\nPort: "+ parameter[2] + "\nUsername: "+ parameter[3] + "\nPassword: "+ parameter[4]
            setKeyboard("YES","NO")
        elif parameter[0]=="4":
            
            
        #else:
            answer = "errore"
    return answer


def setKeyboard(*args):
    keyboard = []
    for arg in args:
        keyboard.append(arg)
    print(keyboard)
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=chat_id, text="Choose wisely", reply_markup=reply_markup)


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
