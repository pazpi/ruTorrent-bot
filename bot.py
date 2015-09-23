# ruTorrent Bot for add torrent to our seedmachine
# command list:
# /magnet to add a magnet link
#
# TO DO:
# make an initial request to set up your personal rutorrent seedmachine
# add more command like:
# /torrent add .torrent file
# /setLabel to insert torrent with that label
# /status to see the status of all existing torrent

import logging, coloredlogs
from logging.handlers import RotatingFileHandler
# requests module for basic http post
import requests
from requests.auth import HTTPBasicAuth
# telegram module for easy work with bot conf
import telegram
# file used to store sensible data, like API key
import config
import init
import telegram_bot
# xmlrpc module for rtorrent communication
import xmlrpc.client
from time import sleep
from _ast import Str
from test.test_ttk_guionly import button

logger = {}
last_update = 0
lastMsgId = 0
botName = 'ruTorrentPy'
token = config.TOKEN
HOST = config.HOST
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /start \n- \n- /help \n- /magnet \n- /host"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/magnet - Add torrent with magnetic link \n/help - This message will be shown \n/info - Show more info about me \n\nFor Example: \n/magnet magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce"

commands = {
'start': '/start',
'info': '/info',
'help': '/help',
'config': '/config'
}

def main(argv=None):
    SetLogger()
    if argv is None or len(argv) <= 1:
        Init()


def SetLogger():
    global logger
    logger = logging.getLogger(__name__)
    # NOSET DEBUG INFO WARNING ERROR CRITICAL
    logger.setLevel(logging.DEBUG)

    # Create a file handler where log is located
    handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024, backupCount=5, encoding=None, delay=0)
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Log inizialized')

def Init():
    global LAST_UPDATE_ID
    # Fetch last message number
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    # Create bot object
    #global bot
    # Creation of bot object
    #bot = telegram.Bot(token)
    # xmlrpc settingsur
    server = xmlrpc.client.ServerProxy(HOST)
    # Get the latest update
    logger.info("-- Init -- LAST_UPDATE_ID: %s", LAST_UPDATE_ID)
    # Infinite Loop
    UpdateLoop(LAST_UPDATE_ID)
    return


def UpdateLoop(LAST_UPDATE_ID):

    # LAST_UPDATE_ID = bot.getUpdates()[-1].update_id  # Get the latest update

    while True:
        try:
            ManageUpdates(LAST_UPDATE_ID)
            sleep(1)
        except Exception:
            # Error
            logging.exception()
    logger.error("Exit from loop!")


def ManageUpdates(LAST_UPDATE_ID):
    # global LAST_UPDATE_ID
    # Fetch last message
    updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    if(not updates):
        logger.error("Couldn't get updates")
        return
    for update in updates:
        command = update.message.text
        chat_id = update.message.chat.id
        update_id = update.update_id
        answer = ''
        init.config_start(chat_id)
        # If newer than the initial
        if LAST_UPDATE_ID < update_id:
            if command:
                answer = GetCommand(command)
                if(answer):
                    bot.sendMessage(chat_id=chat_id, text=answer)
                LAST_UPDATE_ID = update_id

            if LAST_UPDATE_ID < update_id:  # If newer than the initial
                                            # LAST_UPDATE_ID
                if text:
                    rutorrent = magnet(text)
                    bot.sendMessage(chat_id=chat_id, text="Torrent Addedd, Hurray! :D")
                    LAST_UPDATE_ID = update_id

def GetCommand(msg):
    answer = ''
    if(msg):
        par = []
        for item in msg.spit():
            par[item] = msg.spit(item + (+item))
            par[item] = str(par[item])
        #command = msg.split()[:1]
        #command = str(command)
        #host = msg.split()[1:2]
        #username = msg.split()[2:3]
        #password = msg.split()[3:4]
        #host = str(host)
        #command = str(command)
        if("/" in par[0]):
            logger.debug('Command: ' + par[0])
        else:
            logger.debug('Message: ' + str(command))
        if(commands['help'] in par[0]):
            answer = helpTxt
            logger.debug('Answer: helpTxt')
        elif(commands['info'] in par[0]):
            answer = infoTxt
            logger.debug('Answer: infoTxt')
        elif(commands['start'] in par[0]):
            answer = startTxt
            logger.debug('Answer: startTxt')
        elif(par[0][2:8] == 'magnet'):
            addMagnet(par[0])
            answer = 'Magnet added succesfully!'
            logger.debug('Answer: Manget added')
        elif(commands['config'] in par[0]):
            if(par[1] == '[]'):
                answer = config.HOST
                logger.debug('Answer: Host replay')
            else:
                # IMPLEMENT: save host name to file
                HOST = par[1]
                answer = 'Host set'
                logger.debug('Answer: Host set')
            if(par[2] == '[]'):
                answer = config.USERNAME
                logger.debug('Answer: username replay')
            else:
                # IMPLEMENT: save host name to file
                USERNAME = par[2]
                answer = 'Host set'
                logger.debug('Answer: username set')
            if(par[3] == '[]'):
                answer = config.PASSWORD
                logger.debug('Answer: password replay')
            else:
                # IMPLEMENT: save host name to file
                PASSWORD = par[3]
                answer = 'Host set'
                logger.debug('Answer: password set')
        else:
            logger.debug('No command')
    return answer

def addMagnet(torrent):
    torrent = torrent[2:-2]
    url = host + 'ruTorrent/php/addtorrent.php?url=' + torrent
    # Test ArchLinux ISO
    # url = 'http://192.168.1.190/ruTorrent/php/addtorrent.php?url=' + 'magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce'
    requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))

def setKeyboard(*args):
    for arg in args:
        keyboard.append(arg)
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=chat_id, text="Choose wisely", reply_markup=reply_markup)
    


if __name__ == '__main__':
    main()
