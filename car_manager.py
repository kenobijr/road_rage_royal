# importing the module single to be able to change color mode on module level to rgb
import turtle
from turtle import Turtle
from helpers import random_color, gen_ran_y
from screen import SCREEN_WIDTH
# change color mode on module level
turtle.colormode(255)


class CarManager:
    """core game logic creating cars, steering and removing them """
    def __init__(self):
        self.car_container = []
        # value for time.sleep in the main game loop dictating game speed
        self.speed = 0.2
        # distance in px every car does on moving forward one time
        self.move_distance = 5
        # value for upper limit of new generated car batch; increases with game difficulty
        self.car_batch_max = 3
        # gap along x-axis between car batches
        self.car_batch_gap = 80
        # genesis x cor for new car batches
        self.x_gen_cor = (SCREEN_WIDTH / 2) + 20
        # cars going beyond this x cor (out of screen) are wrecked
        self.x_del_cor = -(SCREEN_WIDTH / 2) - 20
        self.add_cars()

    def add_cars(self):
        """if car_container empty, add cars anyway; if cars already exist, only create after certain gap on x-axis"""
        if not self.car_container:
            new_car_positions = self.gen_car_positions(self.car_batch_max)
            self.render_cars(new_car_positions)
        else:
            rightmost_x = max(car.xcor() for car in self.car_container)
            # only add cars after defined gap on x-axis
            if rightmost_x < self.x_gen_cor - self.car_batch_gap:
                new_car_positions = self.gen_car_positions(self.car_batch_max)
                self.render_cars(new_car_positions)

    def gen_car_positions(self, amount_car_range):
        """generating tuples of coordinates of cars along the y-axis preventing overlapping"""
        position_container = []
        # get random y-cor set with no duplicates and out of overlapping range of other y-cor
        ran_y_set = gen_ran_y(amount_car_range=amount_car_range, range_delta=25)
        for y_cor in ran_y_set:
            new_pos_tuple = (self.x_gen_cor, y_cor)
            position_container.append(new_pos_tuple)
        return position_container

    def render_cars(self, positions):
        for car in positions:
            new_car = Turtle("square")
            new_car.penup()
            # stretch it to size 40x20 px as rectangle
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            # retrieving random rgb colors from helpers.py
            new_car.color(random_color())
            new_car.goto(car[0], car[1])
            self.car_container.append(new_car)

    def move_cars(self):
        """move all cars forward´"""
        for car in self.car_container:
            new_x = car.xcor() - self.move_distance
            car.goto(new_x, car.ycor())

    def wreck_cars(self):
        """remove cars crossing the left screen border"""
        for car in self.car_container:
            # check if cars need to be wrecked due to crossing the left screen border
            if car.xcor() < self.x_del_cor:
                del car
