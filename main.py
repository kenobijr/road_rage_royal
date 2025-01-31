from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import time
from screen import init_screen, TOP_BOUNDARY
from turtle import Screen, Turtle


class Game:
    """manages the entire game lifecycle, including initialization, running the game loop, and restarting the game"""
    def __init__(self) -> None:
        self.screen: Screen = init_screen()
        self.player: Player = Player()
        self.cars: CarManager = CarManager()
        self.scoreboard: Scoreboard = Scoreboard()
        # add event listeners for keys
        self.attach_event_listeners()
        # update screen initially
        self.screen.update()

    def run(self) -> None:
        """runs the game loop until the game ends due to an end state"""
        game_is_running: bool = True
        while game_is_running:
            # get value from cars class dictating game speed
            time.sleep(self.cars.speed)
            self.screen.update()
            # move the cars forward; add new cars; remove cars leaving the screen
            self.cars.move_cars()
            self.cars.add_cars()
            self.cars.wreck_cars()
            # check if player crashed with car, game over;
            for car in self.cars.car_container:
                # distance is measuring from the center point of stretched car -> 20px
                if self.player.distance(car) < 20:
                    game_is_running: bool = False
            # check if turtle crossed upper boundary to teleport (top boundary + 10 for half turtle size -2 for 2 lines)
            if self.player.ycor() > TOP_BOUNDARY + 10:
                self.scoreboard.increase_level()
                # teleport player back to start point
                self.player.beam()
                # increase difficulty
                self.cars.car_batch_max += 1
                self.cars.car_batch_min += 1
                self.cars.speed *= 0.9

    def reset(self) -> None:
        """resets the game state for a new game session"""
        self.cars.reset()
        self.player.beam()
        self.scoreboard.reset_level()
        self.attach_event_listeners()

    def attach_event_listeners(self) -> None:
        """adds and activates event listeners for keys"""
        self.screen.listen()
        self.screen.onkey(self.player.move_up, "Up")
        self.screen.onkey(self.player.move_down, "Down")
        self.screen.onkey(self.player.move_right, "Right")
        self.screen.onkey(self.player.move_left, "Left")


    def play(self):
        """starts the game and handles the restart logic"""
        while True:
            # run the main game loop
            self.run()
            continue_or_not: str = self.screen.textinput(
                "Game over",
                "Do you want to play further? Type \"y\" or \"n\": "
            )
            if continue_or_not != "y":
                self.screen.bye()
                break
            # reset the game objects for further round
            self.reset()


def main() -> None:
    """init game screen and objects, sets up event listeners, runs game loop"""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
