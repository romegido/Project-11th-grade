SIZE_LENGTH = 8
SIZE_TO_READ = 1024
IP_FOR_CLIENT = "127.0.0.1"
IP_FOR_SERVER = "0.0.0.0"
PORT = "8820"
commands = {"send picture": "SPT",
            "send grid": "SGD"}


class Grid:
    def __init__(self):
        self.a = [0, 0, 0, 0, 2]
        self.b = [0, 2, 0, 0, 0]
        self.c = [0, 0, 0, 0, 0]
        self.d = [0, 0, 0, 2, 0]
        self.e = [0, 2, 0, 0, 0]
        self.score = 0

    def update_score(self, add):
        self.score += add


def build_message(command, info):
    # get: action to preform, info to send in string
    # return: message by the protocol
    global commands
    message = commands[command] + info
    length = str(len(message))
    message = length.zfill(SIZE_LENGTH) + message
    return message


def send_message(sock, message):
    # get: socket to send to, message to send
    # return:
    sock.send(message.encode())


def get_message(sock):
    # get: socket to get from
    # return: message that was received
    global SIZE_LENGTH
    global SIZE_TO_READ
    message = ""
    length = sock.recv(SIZE_LENGTH)
    i = 0
    while i <= length:
        message += sock.recv(SIZE_TO_READ)
        i += 1
    return message
