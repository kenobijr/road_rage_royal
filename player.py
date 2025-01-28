from turtle import Turtle
# button up moves player 20px forward
MOVE_DISTANCE: int = 10


class Player(Turtle):
    """
    - initiate player inheriting from Turtle class
    - enable moving up and teleporting on level up
    """
    def __init__(self) -> None:
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.goto(0, -270)
        self.setheading(90)

    def move_up(self) -> None:
        """
        moves the player upwards for the defined distance on clicking up key arrow
        """
        new_y: int = int(self.ycor()) + MOVE_DISTANCE
        self.goto(int(self.xcor()), new_y)

    def beam(self) -> None:
        """
        teleports the player to start position again when leveling up
        """
        self.teleport(0, -270)
