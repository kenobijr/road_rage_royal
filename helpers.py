from random import randint
from screen import TOP_BOUNDARY, BOTTOM_BOUNDARY


def random_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b


def gen_ran_y(amount_car_range, range_delta):
    """generate random number of y-cor for cars with no duplicates and no overlapping"""
    # determined by amount_car_range a random number of cars between 0 and range is generated
    amount_cars = randint(0, amount_car_range)
    random_y_set_no_dup = []
    # generate until the target number amount_cars is reached
    while len(random_y_set_no_dup) < amount_cars:
        new_y = randint(BOTTOM_BOUNDARY + 12, TOP_BOUNDARY - 12)
        # Check if new_y is within range_delta of any existing Y-coordinate
        if all(abs(new_y - element) > range_delta for element in random_y_set_no_dup):
            random_y_set_no_dup.append(new_y)
    return random_y_set_no_dup
