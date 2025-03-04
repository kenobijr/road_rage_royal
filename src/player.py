from src.screen import GameScreen
from turtle import Turtle


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
        screen: GameScreen,
        start_x: int = 0,
        start_y: int = -265,
        width: int = 15,
        height: int = 30,
        direction: int = 90,
        move_distance: int = 10
    ) -> None:
        self._turtle_player = Turtle()
        self._turtle_player.shape("assets/car.gif")
        self._turtle_player.penup()
        self._turtle_player.goto(start_x, start_y)
        self._turtle_player.setheading(direction)
        # store relevant properties of player
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.move_distance = move_distance
        # store relevant properties of screen passed in as screen object from main game loop
        self.top_boundary = screen.top_boundary
        self.bottom_boundary = screen.bottom_boundary
        self.right_boundary = screen.right_boundary
        self.left_boundary = screen.left_boundary

    def move_up(self) -> None:
        """
        - moves the player upwards for the defined distance on clicking up key arrow
        - no if-clause to prevent movements over top boundary; this is prevented by teleporting on crossing it
        """
        new_y: int = int(self._turtle_player.ycor()) + self.move_distance
        self._turtle_player.goto(int(self._turtle_player.xcor()), new_y)

    def move_down(self) -> None:
        """
        - moves the player downwards for the defined distance on clicking down key arrow
        - moving below the start threshold at bottom boundary not allowed
        """
        new_y: int = int(self._turtle_player.ycor()) - self.move_distance
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_y >= self.bottom_boundary + (self.height / 2):
            self._turtle_player.goto(int(self._turtle_player.xcor()), new_y)

    def move_right(self) -> None:
        """
        - moves the player right for the defined distance on clicking right key arrow
        - moving beyond the right screen boundary not allowed
        """
        new_x: int = int(self._turtle_player.xcor()) + self.move_distance
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_x <= self.right_boundary - (self.width / 2):
            self._turtle_player.goto(int(new_x), self._turtle_player.ycor())

    def move_left(self) -> None:
        """
        - moves the player left for the defined distance on clicking left key arrow
        - moving beyond the left screen boundary not allowed
        """
        new_x: int = int(self._turtle_player.xcor()) - self.move_distance
        # target ycor is measured from the center of player gif; subtract half player height from it
        if new_x >= self.left_boundary + (self.width / 2):
            self._turtle_player.goto(int(new_x), self._turtle_player.ycor())

    def reset_position(self) -> None:
        """teleports the player to start position again when leveling up"""
        self._turtle_player.teleport(self.start_x, self.start_y)

    def reset(self) -> None:
        """reset player position and shape after collision and player wants further round"""
        self.reset_position()
        self._turtle_player.shape("assets/car.gif")

    def get_ycor(self) -> float:
        """deliver the y-coordinate to outside class callees, since _turtle_player is private"""
        return self._turtle_player.ycor()

    def get_xcor(self) -> float:
        """deliver the x-coordinate to outside class callees, since _turtle_player is private"""
        return self._turtle_player.xcor()

    def get_width(self) -> int:
        """deliver width to outside class callees, since _turtle_player is private"""
        return self.width

    def get_height(self) -> int:
        """deliver height to outside class callees, since _turtle_player is private"""
        return self.height

    def update_shape(self, shape) -> None:
        """update player shape in case of collisions and keep _turtle_player private"""
        self._turtle_player.shape(shape)

