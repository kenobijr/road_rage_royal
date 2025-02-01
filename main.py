from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard, Highscore
import time
from screen import init_screen, attach_event_listeners, TOP_BOUNDARY
from turtle import Screen, Turtle
from helpers import check_collision, collision_animation


class Game:
    """manages the entire game lifecycle, including initialization, running the game loop, and restarting the game"""
    def __init__(self) -> None:
        self.screen: Screen = init_screen()
        self.player: Player = Player()
        self.cars: CarManager = CarManager()
        # shows current level, init with x & y coordinates for position
        self.scoreboard: Scoreboard = Scoreboard(-70, 257)
        self.highscore: Highscore = Highscore(-287, 260)
        # add event listeners for keys
        attach_event_listeners(self.screen, self.player)
        # update screen initially
        self.screen.update()

    def run(self) -> None:
        """
        - runs the game loop until the game ends due to an end state
        - continuously execute game loop with time delay and updating screen
        - update the cars by moving them, adding new batches (when conditions met) and removing ones beyond screen
        - check for end state "player <> car collisions"
        - check if player levels up by reaching top boundary
        """
        game_is_running: bool = True
        while game_is_running:
            # get value from cars class dictating game speed
            time.sleep(self.cars.speed)
            self.screen.update()
            # move the cars forward; add new cars; remove cars leaving the screen
            self.cars.move_cars()
            self.cars.add_cars()
            self.cars.wreck_cars()
            # check for game end state: if player collides with car, end run loop
            if check_collision(self.player, self.cars.car_container):
                # execute animation and time delay
                collision_animation(self.player, self.screen)
                game_is_running: bool = False
            # check if turtle crossed upper boundary to teleport (top boundary + 10 for half turtle size -2 for 2 lines)
            if self.player.ycor() > TOP_BOUNDARY + 10:
                self.scoreboard.increase_level()
                # teleport player back to start point
                self.highscore.update_highscore(self.scoreboard.level)
                self.player.beam()
                # increase difficulty
                self.cars.car_batch_max += 1
                self.cars.car_batch_min += 1
                self.cars.speed *= 0.9

    def reset(self) -> None:
        """resets the game state for a new game session"""
        self.cars.reset()
        self.player.reset()
        self.scoreboard.reset_level()
        attach_event_listeners(self.screen, self.player)

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
