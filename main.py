# main.py
# ruTorrent Bot for add torrent and monitorate your seedmachine
# command list:
# /start
# /help
# /info
# /config
# /hash
#
# TO DO:
# After the description setted with the BotFather user will send the /start command
# Now starts the setting process where the bot will ask first the host, port, user and password for logging in to your rutorrent page.
# Future changes to this setting can be done by using /config where the keyboard change to set HOST and PORT
# So selecting Host bot will ask the url and after that the kwybord return to the sepcific one for config until you select EXIT
# To add magnet you only need to send the magnet link without any command

# add more command like:
# /torrent add .torrent file
# /status to see the status of all existing torrent
# DONE /hash to add a torrent based on his hash
# add the option to have multiple session

import logging, coloredlogs
#import auxiliary_module
from logging.handlers import RotatingFileHandler
# requests module for basic http post
import requests
from requests.auth import HTTPBasicAuth
# telegram module for easy work with bot conf
import telegram
# file used to store sensible data, like API key
import config
import init
import botclass
# xmlrpc module for rtorrent communication
import xmlrpc.client
from time import sleep

logger = {}
last_update = 0
lastMsgId = 0
botName = 'ruTorrentPy'
token = config.TOKEN
HOST = config.HOST
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

commands = {
'start': '/start',
'info': '/info',
'help': '/help',
'config': '/config',
'hash': '/hash'
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
    handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024,
                                  backupCount=5, encoding=None, delay=0)
    handler.setLevel(logging.DEBUG)
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
    handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Log inizialized')

def Init():
    # Create bot object
    global bot
    bot = botclass.Bot()
    #global bot
    # Creation of bot object
    #bot = telegram.Bot(token)
    # Fetch last message number
    #global LAST_UPDATE_ID
    #LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    #LAST_UPDATE_ID = bot.LAST_UPDATE_ID
    # xmlrpc settings
    server = xmlrpc.client.ServerProxy(HOST)
    # Get the latest update
    logger.info("-- Init -- BOT creation")
    # Infinite Loop
    UpdateLoop()
    return


def UpdateLoop():
    while True:
        try:
            ManageUpdates()
            sleep(1)
        except Exception:
            # Error
            #logging.exception()
            logger.error("Exit from loop!")


# def ManageUpdates():
#     # global LAST_UPDATE_ID
#     LAST_UPDATE_ID = bot.LAST_UPDATE_ID
#     # Fetch last message
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
#         # If newer than the initial
#         if LAST_UPDATE_ID < update_id:
#             if command:
#                 answer = GetCommand(command)
#                 if(answer):
#                     bot.sendMessage(chat_id=chat_id, text=answer)
#                 LAST_UPDATE_ID = update_id
# 
#             if LAST_UPDATE_ID < update_id:  # If newer than the initial
#                                             # LAST_UPDATE_ID
#                 if text:
#                     rutorrent = magnet(text)
#                     bot.sendMessage(chat_id=chat_id, text="Torrent Addedd, Hurray! :D")
#                     LAST_UPDATE_ID = update_id


def ManageUpdates():
    # global LAST_UPDATE_ID
    #LAST_UPDATE_ID = bot.LAST_UPDATE_ID
    # Fetch last message
    bot.update()
    answer = ''
    init.config_start(chat_id)
    # If newer than the initial
    if bot.LAST_UPDATE_ID < bot.update_id:
        if bot.command:
            answer = GetCommand(bot.command)
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
        command = msg.split()[:1]
        command = str(command)
        par = msg.split()[1:]
        par = str(par)
        if("/" in command):
            logger.debug('Command: ' + command)
        else:
            logger.debug('Message: ' + command)
        if(commands['help'] in command):
            answer = helpTxt
            logger.debug('Answer: helpTxt')
        elif(commands['info'] in command):
            answer = infoTxt
            logger.debug('Answer: infoTxt')
        elif(commands['start'] in command):
            answer = startTxt
            logger.debug('Answer: startTxt')
        elif(commands['hash'] in command):
            addMagnet(Hash2Magnet(par))
            answer = "Hash added succesfully"
        elif(command[2:8] == 'magnet'):
            addMagnet(command)
            answer = 'Magnet added succesfully!'
            logger.debug('Answer: Manget added')
        elif(commands['host'] in command):
            if(par == '[]'):
                answer = config.HOST
                logger.debug('Answer: Host replay')
            else:
                answer = 'Host set'
                logger.debug('Answer: Host set')
        else:
            answer = 'No command or magnet found'
            logger.debug('No command')
    return answer


def Hash2Magnet(hash):
    magnet = ''
    megnet = "magnet:?xt=urn:btih:" + hash
    return magnet


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
