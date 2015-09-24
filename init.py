"""
Init file

/start -> config bot -> host & port

- Custom keyboard
"""

import telegram
import telegram_bot
import config
import bot

def config_start(chat_id):
    """keyboard_host_port = [[ "HOST", "PORT", "EXIT"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard_host_port)
    bot.sendMessage(chat_id=chat_id, text="Choose wisely", reply_markup=reply_markup)"""
    bot.setKeyboard("HOST", "PORT", "EXIT")
    if (bot.getUpdates(offset=LAST_UPDATE_ID).message.text == "HOST"):
        setHost()
    elif (bot.getUpdates(offset=LAST_UPDATE_ID).message.text == "PORT"):
        setPort()
    elif (bot.getUpdates(offset=LAST_UPDATE_ID).message.text == "EXIT"):
        return
    else:
        return
    
def setHost():
    
    return
    
def setPort():
    
    return