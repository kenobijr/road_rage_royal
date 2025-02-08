from turtle import Turtle
from screen import BOTTOM_BOUNDARY, LEFT_BOUNDARY, RIGHT_BOUNDARY


class Player:
    """
    - initiates a player as composition of Turtle class
    - enables moving and reset on level up
    - args:
        - player direction in degrees
        - player start position x and y coordinates
        - width and height of player gif in px
        - distance player moves in px
    """
    def __init__(
        self,
        start_x: int = 0,
        start_y: int = -265,
        width: int = 15,
        height: int = 30,
        direction: int = 90,
        move_distance: int = 10
    ) -> None:
        self._car = Turtle()
        self._car.shape("car.gif")
        self._car.color("black")
        self._car.penup()
        self._car.goto(start_x, start_y)
        self._car.setheading(direction)

        # store relevant properties
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.move_distance = move_distance

    def move_up(self) -> None:
        """
        moves the player upwards for the defined distance on clicking up key arrow
        """
        new_y: int = int(self._car.ycor()) + self.move_distance
        self._car.goto(int(self._car.xcor()), new_y)

    def move_down(self) -> None:
        """
        - moves the player downwards for the defined distance on clicking down key arrow
        - moving below the start threshold at bottom boundary not allowed
        """
        new_y: int = int(self._car.ycor()) - self.move_distance
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_y >= BOTTOM_BOUNDARY + (self.height / 2):
            self._car.goto(int(self._car.xcor()), new_y)

    def move_right(self) -> None:
        """
        - moves the player right for the defined distance on clicking right key arrow
        - moving beyond the right screen boundary not allowed
        """
        new_x: int = int(self._car.xcor()) + self.move_distance
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_x <= RIGHT_BOUNDARY - (self.width / 2):
            self._car.goto(int(new_x), self._car.ycor())

    def move_left(self) -> None:
        """
        - moves the player left for the defined distance on clicking left key arrow
        - moving beyond the left screen boundary not allowed
        """
        new_x: int = int(self._car.xcor()) - self.move_distance
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_x >= LEFT_BOUNDARY + (self.width / 2):
            self._car.goto(int(new_x), self._car.ycor())

    def reset_position(self) -> None:
        """teleports the player to start position again when leveling up"""
        self._car.teleport(self.start_x, self.start_y)

    def reset(self) -> None:
        """reset player position and shape after collision and player wants further round"""
        self.reset_position()
        self._car.shape("car.gif")

    def get_ycor(self) -> float:
        """deliver the y-coordinate to outside class callees, since _car is private"""
        return self._car.ycor()

    def get_xcor(self) -> float:
        """deliver the x-coordinate to outside class callees, since _car is private"""
        return self._car.xcor()

    def get_width(self) -> int:
        """deliver width to outside class callees, since _car is private"""
        return self.width

    def get_height(self) -> int:
        """deliver height to outside class callees, since _turtle is private"""
        return self.height

    def update_shape(self, shape) -> None:
        """update player shape in case of collisions and keep _car private"""
        self._car.shape(shape)

