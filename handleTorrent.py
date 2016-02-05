# handleTorrent.py
# function to manipulate all the torrent part
#
# import logging, coloredlogs
# import auxiliary_module
# from logging.handlers import RotatingFileHandler
# requests module for basic http post
import requests
from requests.auth import HTTPBasicAuth
import ClassUsers
# telegram module for easy work with bot conf
# import telegram
# file used to store sensible data, like API key
# import config
# import init
# import botDef


def hash2magnet(hash):
    magnet = "magnet:?xt=urn:btih:" + hash[2:-2]
    return magnet


def addmagnet(torrent, chat_id):
    try:
        user = ClassUsers.load(chat_id)
        # http://pazpi.ecc to replace with the setting from the user
        url = user.host + ":" + user.port + '/ruTorrent/php/addtorrent.php?url=' + torrent
        try:
            requests.post(url, auth=HTTPBasicAuth(user.username, user.password))
            return 'Magnet added successfully!'
        except requests.exceptions.ConnectionError:
            return 'Host not reachable'
    except EOFError:
        return 'Host not set, type /start to config your user'
