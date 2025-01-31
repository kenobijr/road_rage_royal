from turtle import Turtle
from screen import BOTTOM_BOUNDARY
# button up moves player 20px forward
MOVE_DISTANCE: int = 10
# width and height of player gif in px
PLAYER_WIDTH: int = 15
PLAYER_HEIGHT: int = 30
# player start position x and y coordinates
PLAYER_START_X: int = 0
PLAYER_START_Y: int = -265
# player direction in degrees
PLAYER_DIRECTION = 90


class Player(Turtle):
    """
    - initiate player inheriting from Turtle class
    - enable moving up and teleporting on level up
    """
    def __init__(self) -> None:
        super().__init__()
        self.shape("car.gif")
        self.color("black")
        self.penup()
        self.goto(PLAYER_START_X, PLAYER_START_Y)
        self.setheading(PLAYER_DIRECTION)

    def move_up(self) -> None:
        """
        moves the player upwards for the defined distance on clicking up key arrow
        """
        new_y: int = int(self.ycor()) + MOVE_DISTANCE
        self.goto(int(self.xcor()), new_y)

    def move_down(self) -> None:
        """
        - moves the player downwards for the defined distance on clicking down key arrow
        - moving below the start threshold at bottom boundary not allowed
        """
        new_y: int = int(self.ycor()) - MOVE_DISTANCE
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_y >= (BOTTOM_BOUNDARY + (PLAYER_HEIGHT / 2)):
            self.goto(int(self.xcor()), new_y)

    def beam(self) -> None:
        """
        teleports the player to start position again when leveling up
        """
        self.teleport(PLAYER_START_X, PLAYER_START_Y)
