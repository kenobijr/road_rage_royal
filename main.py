from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import time
from screen import init_screen, TOP_BOUNDARY
#import sys
#print(sys.executable)


def main() -> None:
    """init screen; init game objects from classes; run game loop"""
    screen = init_screen()
    # create game objects
    player = Player()
    cars = CarManager()
    scoreboard = Scoreboard()
    # render screen manually first time
    screen.update()
    # add event listeners for up key
    screen.listen()
    screen.onkey(player.move_up, "Up")
    # start game loop
    game_is_running = True
    while game_is_running:
        # get value from cars class dictating game speed
        time.sleep(cars.speed)
        screen.update()
        # move the cars forward; add new cars; remove cars leaving the screen
        cars.move_cars()
        cars.add_cars()
        cars.wreck_cars()
        # check if player crashed with car, game over;
        for car in cars.car_container:
            # distance is measuring from the center point of stretched car -> 20px
            if player.distance(car) < 20:
                game_is_running = False
                scoreboard.game_over()
        # check if turtle crossed upper boundary to teleport (top boundary + 10 for half turtle size -2 for 2 lines)
        if player.ycor() > TOP_BOUNDARY + 8:
            scoreboard.increase_level()
            # teleport player back to start point
            player.level_up()
            # increase difficulty
            cars.car_batch_max += 1
            cars.speed *= 0.9
    # let the screen be shown until clicked on it
    screen.exitonclick()


if __name__ == "__main__":
    main()
