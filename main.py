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
#import telegram
# file used to store sensible data, like API key
import config
#import init
import botDef
import handleTorrent
# xmlrpc module for rtorrent communication
import xmlrpc.client
from time import sleep


logger = {}
last_update = 0
lastMsgId = 0
botName = 'ruTorrentPy'
# token = config.TOKEN
# ADDRESS = config.ADDRESS
# USERNAME = config.USERNAME
# PASSWORD = config.PASSWORD

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
    # xmlrpc settings
    # server = xmlrpc.client.ServerProxy(HOST)
    logger.info("-- Init -- BOT creation")
    # Infinite Loop
    UpdateLoop()
    return


def UpdateLoop():
    while True:
        try:
            manageUpdates()
            sleep(1)
        except Exception:
            # Error
            # logging.exception()
            logger.error("Exit from loop!")


def manageUpdates():
    botDef.update()
    answer = ''
    # If newer than the initial
    if botDef.LAST_UPDATE_ID < botDef.update_id:
         if botDef.text:
            answer = getCommand(botDef.text, botDef.chat_id)
            if(answer):
                botDef.bot.sendMessage(chat_id=botDef.chat_id, text=answer)
            botDef.LAST_UPDATE_ID = botDef.update_id


def getCommand(msg,chat_id):
    answer = ''
    logger.debug("file is opening")
    name_file = "chat_id_file/" + str(chat_id)
    f = open(name_file, "w+")
    logger.debug("file creation")
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
            answer = botDef.helpTxt
            logger.debug('Answer: helpTxt')
        elif(commands['info'] in command):
            answer = botDef.infoTxt
            logger.debug('Answer: infoTxt')
        elif(commands['start'] in command):
            answer = botDef.startTxt
            logger.debug('Answer: startTxt')
            botDef.firstConfig() #prova
        elif(commands['hash'] in command):
            handleTorrent.addMagnet(handleTorrent.Hash2Magnet(par))
            answer = "Hash added succesfully"
        elif(command[2:8] == 'magnet'):
            handleTorrent.addMagnet(command)
            answer = 'Magnet added succesfully!'
            logger.debug('Answer: Manget added')
        #elif(commands['config'] in command):
            #botDef.config()
            #firstConfig()
        else:
            answer = 'No command or magnet found. Press /help for the list of the supported commands'
            logger.debug('No command')
        return answer


if __name__ == '__main__':
    main()
