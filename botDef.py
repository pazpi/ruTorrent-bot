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

chat_id_f_config = []
chat_id_config = []
chat_id_host_config = []
chat_id_port_config = []
chat_id_user_config = []
chat_id_passwd_config = []

# def __init__(self):
#     logger = logging.getLogger("telegram_bot.Bot")
#     logger.info("Bot creation")


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
    #print("parameter befor writing: ")
    #print(parameter)
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "w")
    parameter.pop(index)
    parameter.insert(index, data)
    #print("parameter after writing")
    #print(parameter)
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
    if chat_id not in chat_id_f_config:
        chat_id_f_config.append(chat_id)
        answer = "Tell me the host address \n Es: http://myaddress.me"
        writeConfig("0", 0)
    else:
        parameter =[]
        parameter = readConfig()
        #print("par=" + str(parameter))
        #print ("par 0 = " + parameter[0])
        if parameter[0] == "0":
            if not text[:7] == ("http://" or "https:/"): 
                answer = "Address not correct, please follow the example.\nEs: http://myaddress.me"
            else:
                answer = "Tell me the host port \n Es: 8080"
                writeConfig("1", 0)
                writeConfig(text, 1)
        elif parameter[0]=="1":
            if text.isdigit():
                text = int(text)
                if text <= 65536 and text > 0:
                    writeConfig(text, 2)
                    writeConfig("2", 0)
                    answer = "Tell me the host username."
                else:
                    answer = "Out of range.\nMust be between 1 and 65536"
            else:
                answer = "Port not valid.\nEs: 8080"
        elif parameter[0]=="2":
            writeConfig(text, 3)
            writeConfig("3", 0)
            answer = "Tell me the host password"
        elif parameter[0]=="3":
            writeConfig(text, 4)
            writeConfig("4", 0)
            answer = ""
            parameter = readConfig() # rileggo il file altrimenti il campo password rimane quello prima del settaggio
            msg = "Correct? \nAddress: " + parameter[1] + "\nPort: "+ parameter[2] + "\nUsername: "+ parameter[3] + "\nPassword: "+ parameter[4]
            setKeyboard(["YES","NO"], message=msg, chat_id=chat_id, hide=False, exit=False)
        elif parameter[0]=="4":
            if text=="YES":
                msg = "All set, have fun and keep seedind!"
                setKeyboard(message=msg, chat_id=chat_id, hide=True)
            elif text=="NO":
                msg = "Write /config to change settings"
                setKeyboard(message=msg, chat_id=chat_id, hide=True)            
            else:
                msg = "In order to change settings type /config"
                setKeyboard(message=msg, chat_id=chat_id, hide=True)            
            chat_id_f_config.remove(chat_id)
            answer = ""
        else:
            answer = "errore"
    return answer


def setKeyboard(*args, chat_id=chat_id, message="Prova", exit=True, hide=False):
    # *arg must be an array
    if not hide:
        keyboard = []
        for arg in args:
            keyboard.append(arg)
        if exit:
            keyboard.append(["Exit"])
        print(keyboard)
        print(message)
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    else:
        reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text=message, reply_markup=reply_markup)

# Tutta da rivedere, bisogna mettere il numero di chat_id dentro il rispettivo array
# def config():
#     global chat_id
#     global text
#     if chat_id not in chat_id_config:
#         chat_id_config.append(chat_id)
#         msg = "Which parameter you want to change?"
#         setKeyboard(["Host", "Port"], ["Username","Password"], message=msg, chat_id=chat_id, hide=False, exit=True)
#     if text == "Host":
#         if chat_id not in chat_id_config:
#             chat_id_host_config.append(chat_id)
#     elif text == "Port":
#         if chat_id not in chat_id_config:
#             chat_id_port_config.append(chat_id)
#     elif text == "Username":
#         if chat_id not in chat_id_config:
#             chat_id_user_config.append(chat_id)
#     elif text == "Password":
#         if chat_id not in chat_id_config:
#             chat_id_passwd_config.append(chat_id)
#     elif text == "Exit":
#         return ""
#     else:
#         return ""
#     
# 
# def setHost():
#     msg = "Write your host"
#     setKeyboard(message=msg, chat_id=chat_id, hide=True)
#     
#     return ""
# 
# 
# def setPort():
#     msg = "Write your port"
#     setKeyboard(message=msg, chat_id=chat_id, hide=True)
#     return ""
# 
# 
# def setUsername():
#     msg = "Write your username.\nWrite NULL to leave it blank"
#     setKeyboard(message=msg, chat_id=chat_id, hide=True)
#     return ""
# 
# 
# def setPassword():
#     msg = "Write your password.\nWrite NULL to leave it blank"
#     setKeyboard(message=msg, chat_id=chat_id, hide=True)
#     return ""
