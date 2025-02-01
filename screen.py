from turtle import Screen, Turtle
# full width; foremost left x-coordinate is -300, foremost right is 300
SCREEN_WIDTH: int = 600
# full height; foremost bottom y-coordinate is -300, foremost top is 300
SCREEN_HEIGHT: int = 600
# drawn threshold above screen bottom border; player teleports to bottom when crossing it; no cars appear there
TOP_BOUNDARY: int = int((SCREEN_HEIGHT / 2) - 50)
# drawn threshold under screen top border; player cannot move down before crossing it; no cars appear there
BOTTOM_BOUNDARY: int = int(-(SCREEN_HEIGHT / 2) + 60)
# left boundary of screen; player cannot cross it; cars are wrecked after crossing it; added 2px space by testing
LEFT_BOUNDARY: int = int(-(SCREEN_WIDTH / 2)) + 2
# right boundary of screen; player cannot cross it; cars are generated right beyond it; added 4px space by testing
RIGHT_BOUNDARY: int = int(SCREEN_WIDTH / 2) - 4

TEXT_ALIGNMENT: str = "left"
FONT_TYPE: str = "Courier"
FONT_STYLE: str = "normal"


def init_screen() -> Screen:
    """
    - sets up the screen and writes instructions onto it using turtle objects
    - disables automatic screen update, meaning graphics will not be updated in real-time
    - instead screen.update() is used manually within the game loop to refresh the screen and control game speed
    - returns the configured screen object as result
    """
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("ROAD RAGE ROYAL")
    # disables automatic screen updates
    screen.tracer(0)
    # register the player car and explosion gifs as shapes to the screen
    screen.register_shape("car.gif")
    screen.register_shape("explosion.gif")
    # create turtle object to draw instructions / descriptions
    helper = Turtle()
    # draw start line at bottom boundary
    helper.teleport(LEFT_BOUNDARY, BOTTOM_BOUNDARY)
    helper.goto(RIGHT_BOUNDARY, BOTTOM_BOUNDARY)
    # draw finish line at top boundary
    helper.teleport(LEFT_BOUNDARY, TOP_BOUNDARY)
    helper.goto(RIGHT_BOUNDARY, TOP_BOUNDARY)
    # teleport and write text "safe zone" within the starting area
    helper.teleport(150, -280)
    helper.hideturtle()
    helper.penup()
    helper.write("SAFE ZONE", align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, FONT_STYLE))
    # teleport and write text "cross line to teleport" within the finish area
    helper.teleport(120, 260)
    helper.write("TARGET AREA", align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, FONT_STYLE))
    # delete object reference to make garbage collector delete the turtle object
    del helper
    return screen


def attach_event_listeners(screen, player) -> None:
    """adds and activates event listeners for player movement"""
    screen.listen()
    screen.onkey(player.move_up, "Up")
    screen.onkey(player.move_down, "Down")
    screen.onkey(player.move_right, "Right")
    screen.onkey(player.move_left, "Left")
