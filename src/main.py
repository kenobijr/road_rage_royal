from src.player import Player
from src.block_manager import BlockManager
from src.scoreboard import Scoreboard, Highscore
from src.screen import GameScreen
from src.helpers import check_collision, collision_animation
import time
from turtle import Screen
from typing import Dict


class Game:
    """manages the entire game lifecycle, including initialization, running the game loop, and restarting the game"""
    def __init__(self) -> None:
        self.screen: Screen = GameScreen()
        self.player: Player = Player(self.screen)
        self.blocks: BlockManager = BlockManager(self.screen)
        self.scoreboard: Scoreboard = Scoreboard()
        self.highscore: Highscore = Highscore()
        # add event listeners for keys as dict with bound methods to player object
        self._attach_controls()
        # update screen initially
        self.screen.update_screen()
        self.running = True

    def play(self) -> None:
        """starts the game and handles the restart logic"""
        while True:
            # run the main game loop
            self.run()
            if not self._ask_restart():
                break
            # reset the game objects for further round
            self.reset()

    def run(self) -> None:
        """
        - runs the game loop until the game ends due to an end state
        - continuously execute game loop with time delay and updating screen
        - update the blocks by moving them, adding new batches (when conditions met) and removing ones beyond screen
        - check for end state "player <> block collisions"
        - check if player levels up by reaching top boundary
        """
        while self.running:
            # get value from block class dictating game speed
            time.sleep(self.blocks.speed)
            self.screen.update_screen()
            self._update_game_state()
            # check for game end state: if player collides with block, end run loop
            if check_collision(self.player, self.blocks.block_container):
                self._handle_collisions()
                break
            # check if turtle crossed upper boundary (=goal area); if yes level up
            if self._player_reached_goal():
                self._level_up()

    def reset(self) -> None:
        """resets the game state for a new game session"""
        self.blocks.reset()
        self.player.reset()
        self.scoreboard.reset_level()
        self._attach_controls()
        # restart game loop
        self.running = True

    def _attach_controls(self) -> None:
        """attach event handlers to player on init game and restart game"""
        keybindings: Dict = {
            "Up": self.player.move_up,
            "Down": self.player.move_down,
            "Right": self.player.move_right,
            "Left": self.player.move_left
        }
        # use dict as arg to bind keys
        self.screen.attach_event_listeners(keybindings)

    def _update_game_state(self) -> None:
        """handles game state updates per frame (block movement, adding/removing blocks)"""
        self.blocks.update_blocks()

    def _handle_collisions(self) -> None:
        """handles logic when the player collides with a block; sets running flag to false"""
        collision_animation(self.player, self.screen)
        self.running = False

    def _player_reached_goal(self) -> bool:
        """checks if the player has reached the top boundary"""
        return self.player.get_ycor() > self.screen.top_boundary + 10

    def _level_up(self) -> None:
        """handles leveling up logic, updating scores, and increasing difficulty"""
        self.scoreboard.increase_level()
        # update highscore if necessary for new reached level
        self.highscore.update_highscore(self.scoreboard.level)
        self.player.reset_position()
        self.blocks.increase_difficulty(self.scoreboard.level)

    def _ask_restart(self) -> bool:
        """prompts the player to restart the game"""
        response: str = self.screen.show_prompt(
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
