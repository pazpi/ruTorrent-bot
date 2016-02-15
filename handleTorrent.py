# handleTorrent.py
# function to manipulate all the torrent part

import requests
from requests.auth import HTTPBasicAuth
import ClassUsers
# file used to store sensible data, like API key


def hash2magnet(hashlink):
    magnet = "magnet:?xt=urn:btih:" + hashlink[2:-2]
    return magnet


def addmagnet(torrent, chat_id):
    try:
        user = ClassUsers.load(chat_id)
        # http://pazpi.ecc to replace with the setting from the user
        url = user.host + ":" + user.port + '/ruTorrent/php/addtorrent.php?url=' + torrent
        if not (user.username == "NULL" or user.password == "NULL"):
            try:
                respond = requests.post(url, auth=HTTPBasicAuth(user.username, user.password))
                # If server answer correctly answer successfully
                if respond.status_code == 200:
                    return 'Magnet added successfully!'
                else:
                    return 'Error communicating with server Error ' + str(respond.status_code)
            except requests.exceptions.ConnectionError:
                return 'Host not reachable'
        else:
            try:
                respond = requests.post(url)
                if respond.status_code == 200:
                    return 'Magnet added successfully!'
                else:
                    return 'Error communicating with server. Error ' + str(respond.status_code)
            except requests.exceptions.ConnectionError:
                return 'Host not reachable'
    except EOFError:
        return 'Host not set, type /start to config your user'
