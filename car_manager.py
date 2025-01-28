# importing the module single to be able to change color mode on module level to rgb
import turtle
from turtle import Turtle
from helpers import random_color, gen_ran_y
from screen import SCREEN_WIDTH
from typing import List, Tuple
# change color mode on module level
turtle.colormode(255)


class CarManager:
    """
    - core game logic creating cars, steering and removing them
    - game iterations are dictated by screen updating, steered by the self.speed variable setting value for time.sleep
    - every game iteration it is checked, if a new batch of cars is generated
    - a batch of cars is distributed non-overlapping along the y-axis with identical x-coordinate
    - multiple batches have a min. distance non-overlapping between them along the x-axis
    - car batches are generated at a defined genesis point at right side out of screen running from right to left
    - car batches going over the screen on the left side are wrecked
    - on level up difficulty increased by changing self.speed and self.car_batch_max
    """
    def __init__(self) -> None:
        self.car_container: List[Turtle] = []
        # value for time.sleep in main game loop dictating game speed
        self.speed: float = 0.2
        # distance in px of every car moving forward one time
        self.move_distance: int = 5
        # value for upper boundary of new generated car batch; increases with game difficulty
        self.car_batch_max: int = 3
        # gap in px along x-axis between car batches
        self.car_batch_gap: int = 80
        # genesis x cor for new car batches; beyond the screen on the right side
        self.x_genesis_cor: float = (SCREEN_WIDTH / 2) + 20
        # cars going beyond this x cor (out of screen) are wrecked
        self.x_wrecking_cor: float = -(SCREEN_WIDTH / 2) - 20
        # add first batch of cars on initiating car manager
        self.add_cars()

    def add_cars(self) -> None:
        """
        - determines if a new car_batch is added dependent of the state of the existing cars
        - if no cars exist at game start, a new batch is always created
        - if at least one car batch exists, the distance of the rightmost car batch x-coordinate is checked
        - if this distance / gap is big enough, the creation of a further car batch is triggered
        - this way the overlapping of cars along the x-axis is prevented
        """
        # for empty car_container create new batch always
        if not self.car_container:
            new_car_positions: List[Tuple[int, int]] = self.gen_car_positions(self.car_batch_max)
            self.render_cars(new_car_positions)
        else:
            # determine x-coordinate of rightmost car
            rightmost_x: float = max(car.xcor() for car in self.car_container)
            # only add cars after min gap on x-axis
            if rightmost_x < self.x_genesis_cor - self.car_batch_gap:
                new_car_positions: List[Tuple[int, int]] = self.gen_car_positions(self.car_batch_max)
                self.render_cars(new_car_positions)

    def gen_car_positions(self, car_batch_max: int) -> List[Tuple[int, int]]:
        """
        - generates list of tuples with coordinates of cars for a car batch
        - uses helper function gen_ran_y to first receive list of ints for the distributed distinct y-coordinates
        - returns a list of tuples with car coordinates for the batch
        """
        car_coordinates: List[Tuple[int, int]] = []
        # get random amount of y coordinates as list of ints
        car_batch_y_coordinates: List[int] = gen_ran_y(car_batch_max=car_batch_max, min_space=25)
        # generate a coordinate tuple for each y-coordinate and constant genesis x-coordinate
        for y_cor in car_batch_y_coordinates:
            # type casting x-genesis-coordinate into int for consistency
            new_pos_tuple: Tuple[int, int] = (int(self.x_genesis_cor), y_cor)
            car_coordinates.append(new_pos_tuple)
        return car_coordinates

    def render_cars(self, car_coordinates: List[Tuple[int, int]]) -> None:
        """
        - takes list of tuple car-coordinates as input
        - creates cars as turtle objects for each tuple
        - appends each car to self.car_container
        """
        for car in car_coordinates:
            new_car: Turtle = Turtle("square")
            new_car.penup()
            # stretch it to size 40x20 px as rectangle
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            # retrieving random rgb colors from helpers.py
            new_car.color(random_color())
            new_car.goto(car[0], car[1])
            self.car_container.append(new_car)

    def move_cars(self) -> None:
        """
        - move all cars in the car_container forward by reducing the x-coordinate
        - determined by move_distance and self.speed
        """
        for car in self.car_container:
            new_x: float = car.xcor() - self.move_distance
            car.goto(new_x, car.ycor())

    def wreck_cars(self) -> None:
        """
        - delete all cars crossing the left screen border
        - determined by the x-wrecking-coordinate as boundary
        """
        for car in self.car_container:
            # check if cars need to be wrecked due to crossing the left screen border
            if car.xcor() < self.x_wrecking_cor:
                del car
