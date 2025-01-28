from turtle import Turtle
# button up moves player 20px forward
MOVE_DISTANCE: int = 10


class Player(Turtle):
    """initiate player inheriting from Turtle class; enable moving up and teleporting on level up"""
    def __init__(self) -> None:
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.goto(0, -270)
        self.setheading(90)

    def move_up(self) -> None:
        new_y = self.ycor() + MOVE_DISTANCE
        self.goto(self.xcor(), new_y)

    def level_up(self) -> None:
        self.teleport(0, -270)
