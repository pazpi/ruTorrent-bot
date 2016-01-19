import pickle

# status 0: new user
#        1: hostname
#        2: port
#        3: username
#        4: password


class ChatIDUser:
    status = ""
    host = ""
    port = "80"
    username = ""
    password = ""

    def dump(self, chat_id):
        with open("chat_id_file/"+str(chat_id)+'.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)


def load(chat_id):
    with open("chat_id_file/"+str(chat_id)+'.pkl', 'rb') as load_input:
        return pickle.load(load_input)
