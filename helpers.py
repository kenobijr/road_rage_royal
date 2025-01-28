from random import randint
from screen import TOP_BOUNDARY, BOTTOM_BOUNDARY
from typing import List, Tuple


def random_color() -> Tuple[int, int, int]:
    """
    - generates a random RGB color tuple
    - returns:
        Tuple[int, int, int]: a tuple of three integers representing RGB valuess
    """
    r: int = randint(0, 255)
    g: int = randint(0, 255)
    b: int = randint(0, 255)
    return r, g, b


def gen_ran_y(car_batch_max: int, min_space: int) -> List[int]:
    """
    - generate a list of random y-coordinates for a car batch ensuring that:
        1. there are no duplicate y-coordinates
        2. the y-coordinates are spaced apart by certain value to prevent overlapping
    - the amount of cars per batch is a randint between 0 and car_batch_max
    - every single y-coordinate is randomly generated along the y-axis between bottom and top screen boundaries
    args:
    - "car_batch_max": int defining the upper boundary of amount of cars in one batch
    - "min_space": min. space between every y-coordinate to prevent overlapping
    return:
    - list of ints representing the y-coordinates for the car batch
    """
    # define the amount of cars to be generated for the batch
    amount_cars: int = randint(0, car_batch_max)
    car_batch_y_coordinates: List[int] = []
    # generate new y_coordinates until amount_cars is reached
    while len(car_batch_y_coordinates) < amount_cars:
        # adding / subtracting 12 for safety margin from the boundaries due to the car size (height 20 px)
        new_y: int = randint(BOTTOM_BOUNDARY + 12, TOP_BOUNDARY - 12)
        # check for all already generated y-cor in list if the new_y is within min_space
        if all(abs(new_y - element) > min_space for element in car_batch_y_coordinates):
            # only if not "touching" the min_space of any already added y-coordinate, add the new generated y-coordinate
            car_batch_y_coordinates.append(new_y)
    return car_batch_y_coordinates
