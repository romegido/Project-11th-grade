import pygame
import socket


SIZE_LENGTH = 8
SIZE_TO_READ = 1024
IP = "127.0.0.1"
PORT = 8820
DEFAULT = False
BUTTONS = {}
HELP_BUTTON = "WHAT?"
START_BUTTON = "START"
COMP_BUTTON = "COMP"
EXIT_BUTTON = "EXIT"
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
GAME_NAME = "BINARY MERGING"
CMD_SIZE = 3
LEFT = 0
SCROLL = 1
RIGHT = 2
X = 0
Y = 1


def main():
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

    # ------GLOBALS------
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global BUTTONS
    global HELP_BUTTON
    global START_BUTTON
    global COMP_BUTTON

    # ------VARIABLES------
    finish = False
    open_img = "opening_image.jpg"
    help_img = "help_image.jpg"
    start_img = "start_image.jpg"
    comp_img = "comp_image.jpg"
    state_of_screen = ""

    # establishing connection
    sock = socket.socket()
    sock.connect((IP, PORT))

    # getting the opening image
    with open(open_img, "wb") as file:
        message = build_message("", cmd_beginning_picture)
        send_message(sock, message)
        data = receive_bytes_message(sock)
        file.write(data)

    # getting the screen proportions and printing the opening window
    message = build_message("", cmd_proportions)
    send_message(sock, message)
    data = receive_message(sock)
    data = data.split(sep="_")  # (the zero part is the command PPR) first is the width and second is the height
    WINDOW_WIDTH = int(data[1])
    WINDOW_HEIGHT = int(data[2])
    upload_image(open_img)

    # getting the locations of the buttons on the opening screen
    for i in range(4):
        global BUTTONS
        if i == 0:
            global HELP_BUTTON
            message = build_message("", cmd_location_button_1)
            send_message(sock, message)
            data = receive_message(sock)
            data = data.split(sep="_")
            tup = ((int(data[1]), int(data[2])), (int(data[3]), int(data[4])))
            BUTTONS[HELP_BUTTON] = tup
        elif i == 1:
            global START_BUTTON
            message = build_message("", cmd_location_button_2)
            send_message(sock, message)
            data = receive_message(sock)
            data = data.split(sep="_")
            tup = ((int(data[1]), int(data[2])), (int(data[3]), int(data[4])))
            BUTTONS[START_BUTTON] = tup
        elif i == 2:
            global COMP_BUTTON
            message = build_message("", cmd_location_button_3)
            send_message(sock, message)
            data = receive_message(sock)
            data = data.split(sep="_")
            tup = ((int(data[1]), int(data[2])), (int(data[3]), int(data[4])))
            BUTTONS[COMP_BUTTON] = tup
        elif i == 3:
            global EXIT_BUTTON
            message = build_message("", cmd_location_button_4)
            send_message(sock, message)
            data = receive_message(sock)
            data = data.split(sep="_")
            tup = ((int(data[1]), int(data[2])), (int(data[3]), int(data[4])))
            BUTTONS[EXIT_BUTTON] = tup

    # the main loop
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        # here happens the real game
        click = read_mouse_left_click()
        if click != DEFAULT:
            if check_opening_buttons(click) != DEFAULT:
                if check_opening_buttons(click) == HELP_BUTTON:
                    help_screen(help_img, cmd_help_picture, sock)
                    state_of_screen = "help"
                if state_of_screen == "help":
                    pass
                elif check_opening_buttons(click) == START_BUTTON:
                    start_screen(start_img, cmd_start_picture, sock)
                    while True:
                        pass
                elif check_opening_buttons(click) == COMP_BUTTON:
                    comp_screen(comp_img, cmd_competition_picture, sock)
    pygame.quit()
    sock.close()


"""----------GENERAL FUNCTIONS----------"""


def upload_image(name):
    # get: image name to open
    # return:
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global GAME_NAME
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GAME_NAME)
    img = pygame.image.load(name)
    screen.blit(img, (0, 0))
    pygame.display.flip()


"""----------SCREEN FUNCTIONS----------"""


def help_screen(help_img, cmd_help_picture, sock):
    # uploading the help image
    with open(help_img, "wb") as file:
        message = build_message("", cmd_help_picture)
        send_message(sock, message)
        data = receive_bytes_message(sock)
        file.write(data)
    upload_image(help_img)
    state_of_screen = "help"


def start_screen(start_img, cmd_start_picture, sock):
    # starting the game
    with open(start_img, "wb") as file:
        message = build_message("", cmd_start_picture)
        send_message(sock, message)
        data = receive_bytes_message(sock)
        file.write(data)
    upload_image(start_img)


def comp_screen(comp_img, cmd_competition_picture, sock):
    # setting up the competition
    with open(comp_img, "wb") as file:
        message = build_message("", cmd_competition_picture)
        send_message(sock, message)
        data = receive_bytes_message(sock)
        file.write(data)
    upload_image(comp_img)


"""----------MOUSE FUNCTIONS----------"""


def read_mouse_left_click():
    # get:
    # return: (x, y) tuple if was left click and DEFAULT otherwise
    states = pygame.mouse.get_pressed(num_buttons=3)
    global LEFT
    if states[LEFT]:
        return pygame.mouse.get_pos()
    else:
        global DEFAULT
        return DEFAULT


def check_pos_valid(actual, dot1, dot2):
    # get: tuple with x&y values to compare, dot1 and dot2 are tuples with (x, y) and are the boundaries
    #                                        note: dot1 is upper left, dot2 is bottom right of a rectangle
    # return: True if within the values and False otherwise
    global X
    global Y
    global DEFAULT
    if dot1[X] <= actual[X] <= dot2[X]:
        if dot1[Y] <= actual[Y] <= dot2[Y]:
            return True
        else:
            return DEFAULT
    else:
        return DEFAULT


def check_opening_buttons(click):
    # get: click of mouse
    # return: the name of the button that was clicked or DEFAULT otherwise
    global HELP_BUTTON
    global START_BUTTON
    global COMP_BUTTON
    global BUTTONS
    global DEFAULT
    if check_pos_valid(click, BUTTONS[HELP_BUTTON][0], BUTTONS[HELP_BUTTON][1]):
        return HELP_BUTTON
    if check_pos_valid(click, BUTTONS[START_BUTTON][0], BUTTONS[START_BUTTON][1]):
        return START_BUTTON
    if check_pos_valid(click, BUTTONS[COMP_BUTTON][0], BUTTONS[COMP_BUTTON][1]):
        return COMP_BUTTON
    else:
        return DEFAULT


def check_if_exit_button(click):
    # get: click of a mouse
    # return: True if clicked where the exit button is located and DEFAULT otherwise
    global BUTTONS
    global EXIT_BUTTON
    global DEFAULT
    if check_pos_valid(click, BUTTONS[EXIT_BUTTON][0], BUTTONS[EXIT_BUTTON][1]):
        return True
    else:
        return DEFAULT


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
    main()
