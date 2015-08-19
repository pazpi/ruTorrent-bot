# ruTorrent Bot for add torrent to our seedmachine
# command list:
# /magnet to add a magnet link
#
# TO DO:
# add more command, like
# /torrent add torrent file
# /setLabel to insert torrent with that label

#import urllib
import requests

import telegram
#from urllib import request


def main():
    # Telegram Bot Authorization Token
    bot = telegram.Bot(token='90993397:AAFL3eonfG3yrgRynlCLaE0H9Mlkam6J9BA')

    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id  # Get the latest update

    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
    	text = update.message.text
    	chat_id = update.message.chat.id
      update_id = update.update_id

		if LAST_UPDATE_ID <= update_id:

      	if text:
         	rutorrent = magnet(text)
            bot.sendMessage(chat_id=chat_id, text=rutorrent)
            bot.sendMessage(chat_id=chat_id, text="Torrent Added!")
            LAST_UPDATE_ID = update_id


def magnet(text):
    url = 'http://192.168.1.190/ruTorrent/php/addtorrent.php?url=' + 'magnet:?xt=urn:btih:828e86180150213c10677495565baef6b232dbdd&dn=archlinux-2015.08.01-dual.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce'
    #data = urllib.urlparse(url)
    requests.post(url)
    #return data.strip()

if __name__ == '__main__':
    main()
