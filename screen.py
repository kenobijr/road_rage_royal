from turtle import Screen, Turtle

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TOP_BOUNDARY = 250
BOTTOM_BOUNDARY = -240

TEXT_ALIGNMENT = "left"
FONT_TYPE = "Courier"
FONT_STYLE = "normal"


def init_screen():
    """managing screen logic and write instructions (all but gameboard)"""
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("A turtle crossing tale...")
    screen.tracer(0)
    # draw start and end line
    helper = Turtle()
    helper.teleport(-300, BOTTOM_BOUNDARY)
    helper.goto(300, BOTTOM_BOUNDARY)
    helper.teleport(-300, TOP_BOUNDARY)
    helper.goto(300, TOP_BOUNDARY)
    # write safe_zone and teleport
    helper.teleport(150, -280)
    helper.hideturtle()
    helper.penup()
    helper.write("SAFE ZONE", align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, FONT_STYLE))
    helper.teleport(50, 265)
    helper.write("Cross line to teleport", align=TEXT_ALIGNMENT, font=(FONT_TYPE, 18, FONT_STYLE))
    # delete object reference to make garbage collector delete the turtle object
    del helper
    return screen
