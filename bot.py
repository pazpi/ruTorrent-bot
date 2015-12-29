# ruTorrent Bot for add torrent and monitor your seedmachine
# command list:
# /help
# /info
# /config
#
# TO DO:
# After the description setted with the BotFather user will send the /start command
# Now starts the setting process where the bot will ask first the host, port, user and password for logging in to your
# rutorrent page.
# Future changes to this setting can be done by using /config where the keyboard change to set HOST and PORT
# So selecting Host, bot will ask the url and after that the keyboard return to the specific one for config until you
# select EXIT
# To add magnet you only need to send the magnet link without any command

# add more command like:
# /torrent add .torrent file
# /status to see the status of all existing torrent
# /hash to add a torrent based on his hash
# add the option to have multiple session

import logging
from logging.handlers import RotatingFileHandler
# requests module for basic http post
from requests.auth import HTTPBasicAuth
# telegram module for easy work with bot conf
import telegram
# file used to store sensible data, like API key
import config
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
startTxt = "Hi! I'm a bot developed by @pazpi and @martinotu to add torrent to your seedmachine \nAvailable commands: \n- /start \n- /help \n- /info \n- /host"
infoTxt = "Authors: @pazpi @martinotu \nGithub: https://github.com/pazpi/ruTorrent-bot \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. And remember: keep seeding!"
helpTxt = "ruTorrentPyBot \n\nAdd torrent directly from telegram. \n\n Commands: \n/magnet - Add torrent with magnetic link \n/help - This message will be shown \n/info - Show more info about me \n\nFor Example: \n/magnet magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce"

commands = {
    'start': '/start',
    'info': '/info',
    'help': '/help',
    'host': '/host',
    'config': '/config',
    'hash': '/hash'
}


def main(argv=None):
    setlogger()
    if argv is None or len(argv) <= 1:
        init()


def setlogger():
    global logger
    logger = logging.getLogger(__name__)
    # NOSET DEBUG INFO WARNING ERROR CRITICAL
    logger.setLevel(logging.DEBUG)

    # Create a file handler where log is located
    handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024, backupCount=5, encoding=None,
                                  delay=0)
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Log initialized')


def init():
    # Create bot object
    global bot
    # Creation of bot object
    bot = telegram.Bot(token)
    # Fetch last message number
    global LAST_UPDATE_ID
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    # xmlrpc settings
    # server = xmlrpc.client.ServerProxy(HOST)
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
            # logging.exception()
            logger.error("Exit from loop!")


def ManageUpdates():
    global LAST_UPDATE_ID
    logger.info("LAST_UPDATE_ID: %s", LAST_UPDATE_ID)
    updates = bot.getUpdates(offset=LAST_UPDATE_ID)
    if (not updates):
        logger.error("Couldn't get updates")
        return
    for update in updates:
        command = update.message.text
        chat_id = update.message.chat.id
        update_id = update.update_id
        # answer = ''
        # If newer than the initial
        if LAST_UPDATE_ID < update_id:
            if command:
                answer = GetCommand(command)
                if (answer):
                    bot.sendMessage(chat_id=chat_id, text=answer)
                LAST_UPDATE_ID = update_id


def GetCommand(msg):
    answer = ''
    if (msg):
        command = msg.split()[:1]
        command = str(command)
        host = msg.split()[1:]
        host = str(host)
        if ("/" in command):
            logger.debug('Command: ' + command)
        else:
            logger.debug('Message: ' + command)
        if (commands['help'] in command):
            answer = helpTxt
            logger.debug('Answer: helpTxt')
        elif (commands['info'] in command):
            answer = infoTxt
            logger.debug('Answer: infoTxt')
        elif (commands['start'] in command):
            answer = startTxt
            logger.debug('Answer: startTxt')
        elif (commands['hash'] in command):
            addMagnet(Hash2Magnet(host))
            answer = "Hash added succesfully"
        elif (command[2:8] == 'magnet'):
            addMagnet(command)
            answer = 'Magnet added succesfully!'
            logger.debug('Answer: Manget added')
        elif (commands['host'] in command):
            if (host == '[]'):
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
    magnet = "magnet:?xt=urn:btih:" + hash
    return magnet


def addMagnet(torrent):
    torrent = torrent[2:-2]
    url = host + 'ruTorrent/php/addtorrent.php?url=' + torrent
    # Test ArchLinux ISO
    # url = 'http://192.168.1.190/ruTorrent/php/addtorrent.php?url=' + 'magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce'
    requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))


if __name__ == '__main__':
    main()
