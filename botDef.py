# botDef.py
# telegram module for easy work with bot conf
import telegram
# file used to store sensible data, like API key
import token
import logging
import ClassUsers

logger = logging.getLogger(__name__)

startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \n" \
           "Available commands: \n- /help \n- /info \n- /hash"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \n" \
          "By using this bot you agree that your doing so at your own risk. Authors will not be responsible for any " \
          "choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/help - Show this message\n" \
          "/info - Show more info about me \n/hash - To add a torrent from his hash\n\n" \
          "To add a torrent from his magnet link just sent the link :D\n\n"

bot = telegram.Bot(token.TOKEN)
text = ''
chat_id = ''
update_id = ''
username = ''
LAST_UPDATE_ID = bot.getUpdates()[-1].update_id

chat_id_f_config = []
chat_id_config = []
chat_id_host_config = []
chat_id_port_config = []
chat_id_user_config = []
chat_id_password_config = []


# def __init__(self):
#     logger = logging.getLogger("telegram_bot.Bot")
#     logger.info("Bot creation")


def update():
    updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    global text
    global chat_id
    global update_id
    global username
    for update_data in updates:
        text = update_data.message.text
        chat_id = update_data.message.chat.id
        update_id = update_data.update_id


def read_user_info():
    global chat_id
    user = ClassUsers.load(chat_id)
    return user


def readconfig():
    parameter = ["", "", "", "", "", ""]
    global chat_id
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "r")  # doesn't create the file
    for i in range(6):
        parameter[i] = f.readline()[:-1]
        # print(parameter[i])
    f.close()
    return parameter


def write_user_info(user):
    global chat_id
    user.dump(chat_id)


def writeconfig(data, index):
    global chat_id
    user = read_user_info()
    if index == 0:
        user.status = data
    elif index == 1:
        user.host = data
    elif index == 2:
        user.port = data
    elif index == 3:
        user.username = data
    elif index == 4:
        user.password = data
    user.dump(chat_id)
    # parameter = readconfig()
    # print("parameter before writing: ")
    # print(parameter)
    # name_file = "chat_id_file/" + str(chat_id)
    # f = open(name_file, "w")
    # parameter.pop(index)
    # parameter.insert(index, data)
    # print("parameter after writing")
    # print(parameter)
    # f.close()
    # name_file = "chat_id_file/" + str(chat_id)
    # f = open(name_file, "w")
    # f.write('\n'.join(str(line) for line in parameter))
    # f.close()


def firstconfig():
    global chat_id
    global text
    if chat_id not in chat_id_f_config:
        chat_id_f_config.append(chat_id)
        answer = "Tell me the host address \n Es: http://myaddress.me"
        writeconfig("0", 0)
    else:
        user = read_user_info()
        if user.status == "0":
            if not text[:7] == ("http://" or "https:/"):
                answer = "Address not correct, please follow the example.\nEs: http://myaddress.me"
            else:
                answer = "Tell me the host port \n Es: 8080"
                writeconfig("1", 0)
                writeconfig(text, 1)
        elif user.status == "1":
            if text.isdigit():
                if 65536 >= text > 0:
                    writeconfig(text, 2)
                    writeconfig("2", 0)
                    answer = "Tell me the host username."
                else:
                    answer = "Out of range.\nMust be between 1 and 65536"
            else:
                answer = "Port not valid.\nEs: 8080"
        elif user.status == "2":
            writeconfig(text, 3)
            writeconfig("3", 0)
            answer = "Tell me the host password"
        elif user.status == "3":
            writeconfig(text, 4)
            writeconfig("4", 0)
            user = read_user_info()
            # parameter = readconfig() # read the file again to update the password data
            msg = "Correct? \nAddress: " + user.host + "\nPort: " + user.port + "\nUsername: " + user.username + \
                  "\nPassword: " + user.password
            setkeyboard(["YES", "NO"], message=msg, chat_id=chat_id, hide=False, is_exit=False)
            answer = ""
        elif user.status == "4":
            if text == "YES":
                msg = "All set, have fun and keep seeding!"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
            elif text == "NO":
                msg = "Write /config to change settings"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
            else:
                msg = "In order to change settings type /config"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
            chat_id_f_config.remove(chat_id)
            answer = ""
        else:
            answer = "error"
    return answer


def setkeyboard(*args, chat_id=chat_id, message="Prova", is_exit=True, hide=False):
    # *arg must be an array
    if not hide:
        keyboard = []
        for arg in args:
            keyboard.append(arg)
        if is_exit:
            keyboard.append(["Exit"])
        # print(keyboard)
        # print(message)
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    else:
        reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text=message, reply_markup=reply_markup)


def config():
    global chat_id
    global text
    global chat_id_host_config
    if chat_id not in chat_id_config:
        chat_id_config.append(chat_id)
        msg = "Which parameter you want to change?"
        setkeyboard(["Host", "Port"], ["Username", "Password"], message=msg, chat_id=chat_id, hide=False, is_exit=True)
    else:
        # User has type something form the custom keyboard
        if text == "Host":
            if chat_id not in chat_id_host_config:
                chat_id_host_config.append(chat_id)
                print(chat_id_host_config)
                msg = "Write your host"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
        elif text == "Port":
            if chat_id not in chat_id_port_config:
                chat_id_port_config.append(chat_id)
                msg = "Write your port"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
        elif text == "Username":
            if chat_id not in chat_id_user_config:
                chat_id_user_config.append(chat_id)
                msg = "Write your username.\nWrite NULL to leave it blank"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
        elif text == "Password":
            if chat_id not in chat_id_password_config:
                chat_id_password_config.append(chat_id)
                msg = "Write your password.\nWrite NULL to leave it blank"
                setkeyboard(message=msg, chat_id=chat_id, hide=True)
        elif text == "Exit":
            chat_id_config.remove(chat_id)
            msg = "Config ended"
            setkeyboard(message=msg, chat_id=chat_id, hide=True)
            return ""
        else:
            logger.debug("error config")
            return ""


def sethost():
    global text
    global chat_id
    print("called sethost")
    if not text[:7] == ("http://" or "https:/"):
        return "Address not correct, please follow the example.\nEs: http://myaddress.me"
    else:
        chat_id_host_config.remove(chat_id)
        try:
            user = ClassUsers.load(chat_id)
        except EOFError:
            user = ClassUsers.ChatIDUser()
        user.host = text
        user.dump(chat_id)
        chat_id_config.remove(chat_id)
        return "Host address setted"


def setport():
    global text
    global chat_id
    print("called setport")
    if not text.isdigit:
        return "Port not correct, make sure is a number.\nEs: 80, 8080"
    else:
        chat_id_port_config.remove(chat_id)
        user = ClassUsers.load(chat_id)
        user.port = text
        user.dump(chat_id)
        chat_id_config.remove(chat_id)
        return "Port setted"


def setusername():
    global text
    global chat_id
    print("called setusername")
    chat_id_user_config.remove(chat_id)
    user = ClassUsers.load(chat_id)
    user.hostname = text
    user.dump(chat_id)
    chat_id_config.remove(chat_id)
    return "Hostname setted"


def setpassword():
    global text
    global chat_id
    print("called setusername")
    chat_id_password_config.remove(chat_id)
    user = ClassUsers.load(chat_id)
    user.password = text
    user.dump(chat_id)
    chat_id_config.remove(chat_id)
    return "Password setted"
