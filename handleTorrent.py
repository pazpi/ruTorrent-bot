# handleTorrent
# function to manipulate all the torrent part

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

def Hash2Magnet(hash):
    magnet = ''
    magnet = "magnet:?xt=urn:btih:" + hash[2:-2]
    return magnet


def addMagnet(torrent):
    url =  "http://pazpi.noip.me:8080/" + 'ruTorrent/php/addtorrent.php?url=' + torrent #pazpi.ecc to replace with the setting from the user
    # print(url)
    # Test ArchLinux ISO
    # url = 'http://192.168.1.190/ruTorrent/php/addtorrent.php?url=' + 'magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce'
    requests.post(url, auth=HTTPBasicAuth("",""))
