import pickle
import logging
user_logger = logging.getLogger("main.classUsers")
# status 0: new user
#        1: hostname
#        2: port
#        3: username
#        4: password


class ChatIDUser:
    status = "-1"
    host = ""
    port = "80"
    username = ""
    password = ""

    def dump(self, chat_id):
        with open("chat_id_file/"+str(chat_id)+'.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
            user_logger.debug("dump success")


def load(chat_id):
    with open("chat_id_file/"+str(chat_id)+'.pkl', 'rb') as load_input:
        user_logger.debug("load success")
        return pickle.load(load_input)


