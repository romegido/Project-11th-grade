import protocol
import socket


LEFT = 0
SCROLL = 1
RIGHT = 2
X = 0
Y = 1
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_NAME = "BINARY MERGING"
OPENING_IMAGE = "opening.jpg"
DEFAULT = False
BUTTONS = {"WHAT?": ((104, 507), (374, 625)),
           "START": ((505, 507), (775, 625)),
           "COMP": ((893, 507), (1162, 625))}


def main():
    """-------VARIABLES-------"""
    global DEFAULT
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global GAME_NAME
    finish = False
    help_image = "help.jpg"
    start_image = "start.jpg"
    comp_image = "comp.jpg"
    """-----------------------"""

    """-------MAIN LOOP-------"""
    # running as long as didn't click on the X button
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            else:
                # here happens the real game
                click = read_mouse_left_click()
                if click != DEFAULT:
                    if check_opening_buttons(click) != DEFAULT:
                        if check_opening_buttons(click) == "WHAT?":
                            # uploading the help image
                            upload_image(help_image)
                        elif check_opening_buttons(click) == "START":
                            # starting the game
                            upload_image(start_image)
                        elif check_opening_buttons(click) == "COMP":
                            # setting up the competition
                            upload_image(comp_image)
    pygame.quit()


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
    global BUTTONS
    global DEFAULT
    if check_pos_valid(click, BUTTONS["WHAT?"][0], BUTTONS["WHAT?"][1]):
        return "WHAT?"
    if check_pos_valid(click, BUTTONS["START"][0], BUTTONS["START"][1]):
        return "START"
    if check_pos_valid(click, BUTTONS["COMP"][0], BUTTONS["COMP"][1]):
        return "COMP"
    else:
        return DEFAULT


"""----------BUTTONS FUNCTIONS----------"""

if __name__ == "__main__":
    # connecting to client
    pygame.init()
    upload_image(OPENING_IMAGE)

    main()