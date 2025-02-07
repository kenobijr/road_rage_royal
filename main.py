from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard, Highscore
import time
from screen import init_screen, attach_event_listeners, TOP_BOUNDARY
from turtle import Screen
from helpers import check_collision, collision_animation


class Game:
    """manages the entire game lifecycle, including initialization, running the game loop, and restarting the game"""
    def __init__(self) -> None:
        self.screen: Screen = init_screen()
        self.player: Player = Player()
        self.cars: CarManager = CarManager()
        self.scoreboard: Scoreboard = Scoreboard(-70, 257)
        self.highscore: Highscore = Highscore(-287, 260)
        # add event listeners for keys
        attach_event_listeners(self.screen, self.player)
        # update screen initially
        self.screen.update()
        self.running = True

    def run(self) -> None:
        """
        - runs the game loop until the game ends due to an end state
        - continuously execute game loop with time delay and updating screen
        - update the cars by moving them, adding new batches (when conditions met) and removing ones beyond screen
        - check for end state "player <> car collisions"
        - check if player levels up by reaching top boundary
        """
        while self.running:
            # get value from cars class dictating game speed
            time.sleep(self.cars.speed)
            self.screen.update()
            self._update_game_state()
            # check for game end state: if player collides with car, end run loop
            if check_collision(self.player, self.cars.car_container):
                self._handle_collisions()
                break
            # check if turtle crossed upper boundary (=goal area); if yes level up
            if self._player_reached_goal():
                self._level_up()

    def _update_game_state(self):
        """handles game state updates per frame (car movement, adding/removing cars)"""
        self.cars.update_cars()

    def _handle_collisions(self):
        """handles logic when the player collides with a car; sets running flag to false"""
        collision_animation(self.player, self.screen)
        self.running = False

    def _player_reached_goal(self):
        """checks if the player has reached the top boundary"""
        return self.player.get_ycor() > TOP_BOUNDARY + 10

    def _level_up(self):
        """handles leveling up logic, updating scores, and increasing difficulty"""
        self.scoreboard.increase_level()
        # update highscore if necessary for new reached level
        self.highscore.update_highscore(self.scoreboard.level)
        self.player.reset_position()
        self.cars.increase_difficulty(self.scoreboard.level)

    def reset(self) -> None:
        """resets the game state for a new game session"""
        self.cars.reset()
        self.player.reset()
        self.scoreboard.reset_level()
        attach_event_listeners(self.screen, self.player)
        # restart game loop
        self.running = True

    def play(self):
        """starts the game and handles the restart logic"""
        while True:
            # run the main game loop
            self.run()
            if not self._ask_restart():
                self.screen.bye()
                break
            # reset the game objects for further round
            self.reset()

    def _ask_restart(self) -> bool:
        """prompts the player to restart the game"""
        response: str = self.screen.textinput(
                "Game over",
                "Do you want to play further? Type \"y\" or \"n\": "
        )
        return response.lower() == "y" if response else False

def main() -> None:
    """init game screen and objects, sets up event listeners, runs game loop"""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
