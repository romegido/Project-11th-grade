import socket
import threading

SIZE_LENGTH = 8
SIZE_TO_READ = 1024
PORT = 8820
IP = "0.0.0.0"
CMD_SIZE = 3
NUM_OF_START_IMGS = 10
IMGS_EXTENSION = "jpg"
DIR = "imgs\\"


def main(client_sock):
    # ------COMMANDS------
    cmd_beginning_picture = "BPT"
    cmd_proportions = "PPR"
    cmd_location_button_1 = "OB1"
    cmd_location_button_2 = "OB2"
    cmd_location_button_3 = "OB3"
    cmd_location_button_4 = "OB4"
    cmd_help_picture = "HPT"
    cmd_start_picture = "SPT"
    cmd_competition_picture = "CMP"

    # ------VARIABLES------
    opening_img = "imgs\\opening.jpg"
    help_img = "imgs\\help.jpg"
    start_img = "imgs\\start"
    comp_img = "imgs\\comp.jpg"
    window_width = 1280
    window_height = 710
    help_button = "WHAT?"
    start_button = "START"
    comp_button = "COMP"
    exit_button = "EXIT"
    buttons = {help_button: ((104, 507), (374, 625)),
               start_button: ((505, 507), (775, 625)),
               comp_button: ((893, 507), (1162, 625)),
               exit_button: ((25, 19), (93, 85))}

    try:
        while True:
            message = receive_message(client_sock)
            message = message.split(sep="_")
            if message[0] == cmd_beginning_picture:
                with open(opening_img, "rb") as file:
                    pic = file.read()
                message = build_bytes_message(pic, cmd_beginning_picture)
                send_bytes_message(client_sock, message)
            elif message[0] == cmd_proportions:
                message = str(window_width) + "_" + str(window_height)
                message = build_message(message, cmd_proportions)
                send_message(client_sock, message)
            elif message[0] == cmd_location_button_1:
                message = str(buttons[help_button][0][0]) + "_" + str(buttons[help_button][0][1])
                message += "_" + str(buttons[help_button][1][0]) + "_" + str(buttons[help_button][1][1])
                message = build_message(message, cmd_location_button_1)
                send_message(client_sock, message)
            elif message[0] == cmd_location_button_2:
                message = str(buttons[start_button][0][0]) + "_" + str(buttons[start_button][0][1])
                message += "_" + str(buttons[start_button][1][0]) + "_" + str(buttons[start_button][1][1])
                message = build_message(message, cmd_location_button_2)
                send_message(client_sock, message)
            elif message[0] == cmd_location_button_3:
                message = str(buttons[comp_button][0][0]) + "_" + str(buttons[comp_button][0][1])
                message += "_" + str(buttons[comp_button][1][0]) + "_" + str(buttons[comp_button][1][1])
                message = build_message(message, cmd_location_button_3)
                send_message(client_sock, message)
            elif message[0] == cmd_location_button_4:
                message = str(buttons[exit_button][0][0]) + "_" + str(buttons[exit_button][0][1])
                message += "_" + str(buttons[exit_button][1][0]) + "_" + str(buttons[exit_button][1][1])
                message = build_message(message, cmd_location_button_4)
                send_message(client_sock, message)
            elif message[0] == cmd_help_picture:
                with open(help_img, "rb") as file:
                    pic = file.read()
                message = build_bytes_message(pic, cmd_help_picture)
                send_bytes_message(client_sock, message)
            elif message[0] == cmd_start_picture:
                start_img = generate_start_img(start_img)
                with open(start_img, "rb") as file:
                    pic = file.read()
                message = build_bytes_message(pic, cmd_start_picture)
                send_bytes_message(client_sock, message)
            elif message[0] == cmd_competition_picture:
                with open(comp_img, "rb") as file:
                    pic = file.read()
                message = build_bytes_message(pic, cmd_competition_picture)
                send_bytes_message(client_sock, message)
    except Exception as error:
        client_sock.close()
        print("Disconnected from client: ", error)


"""----------GENERAL FUNCTIONS----------"""


def generate_start_img(base):
    # get: base name of start image (supposed to be 'start')
    # return: the name of a random start image that was generated
    import random
    global NUM_OF_START_IMGS
    global IMGS_EXTENSION
    num = random.randint(1, NUM_OF_START_IMGS)
    file_name = base + str(num) + "." + IMGS_EXTENSION
    return file_name


"""----------COMMUNICATION FUNCTIONS----------"""


def receive_message(sock):
    # get: socket
    # return: message from socket
    global SIZE_LENGTH
    global SIZE_TO_READ
    message = ""
    length = int(sock.recv(SIZE_LENGTH).decode())
    i = 0
    while i <= length:
        message += sock.recv(SIZE_TO_READ).decode()
        i += SIZE_TO_READ
    return message


def send_message(sock, message):
    # get: socket and a message
    # return:
    sock.send(message.encode())


def send_bytes_message(sock, message):
    # get: socket and a message in bytes
    # return:
    sock.send(message)


def receive_bytes_message(sock):
    # get: socket
    # return: message from socket
    global SIZE_LENGTH
    global SIZE_TO_READ
    global CMD_SIZE
    message = b''
    length = int(sock.recv(SIZE_LENGTH).decode())
    cmd = sock.recv(CMD_SIZE + 1).decode()
    length = length - CMD_SIZE - 1
    i = 0
    while i <= length:
        message += sock.recv(SIZE_TO_READ)
        i += SIZE_TO_READ
    return message


def build_message(info, cmd):
    # get: action to preform, info to send in string
    # return: message by the protocol
    global SIZE_LENGTH
    message = cmd + "_" + info
    length = str(len(message))
    message = length.zfill(SIZE_LENGTH) + message
    return message


def build_bytes_message(info, cmd):
    # get: action to preform, info to send in bytes
    # return: message list by the protocol
    global SIZE_LENGTH
    message = cmd.encode() + "_".encode() + info
    message = str(len(message)).zfill(SIZE_LENGTH).encode() + message
    return message


if __name__ == "__main__":
    try:
        server_socket = socket.socket()
        server_socket.bind((IP, PORT))
        server_socket.listen()
        print("-------SERVER IS UP AND RUNNING !-------\r\n")
        while True:
            client_socket, client_address = server_socket.accept()
            print("-------CONNECTED TO CLIENT-------")
            t = threading.Thread(target=main, args=(client_socket,))
            t.start()
    except Exception as error:
        print(error)
