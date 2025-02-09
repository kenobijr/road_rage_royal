from turtle import Turtle
from highscore_db import HighscoreDB

TEXT_ALIGNMENT: str = "left"
FONT_TYPE: str = "Courier"


class Scoreboard:
    """manage the scoreboard logic showing the level of the current game"""
    def __init__(self, start_x: int, start_y: int) -> None:
        self.level: int = 1
        self._turtle = Turtle()
        self._turtle.penup()
        self._turtle.hideturtle()
        self._turtle.goto(start_x, start_y)
        self.render_level()

    def render_level(self) -> None:
        """render the current level to the UI"""
        level: str = f"Level {self.level}"
        self._turtle.write(level, align=TEXT_ALIGNMENT, font=(FONT_TYPE, 30, "bold"))

    def increase_level(self) -> None:
        """update level counter and UI"""
        self.level += 1
        self._turtle.clear()
        self.render_level()

    def reset_level(self) -> None:
        """reset level after game restart"""
        self.level: int = 1
        self._turtle.clear()
        self.render_level()


class Highscore:
    """manages the highscore logic showing and updating the highscore over all games played using sqlite3 DB"""
    def __init__(self, start_x: int, start_y: int) -> None:
        # initiate & set up sqlite3 DB initially with default value 1 if not already existing
        self.highscore_db = HighscoreDB()
        # reads highscore from DB
        self.highscore = self.highscore_db.get_highscore()
        self._turtle = Turtle()
        self._turtle.penup()
        self._turtle.hideturtle()
        self._turtle.goto(start_x, start_y)
        self.render_highscore()

    def update_highscore(self, level):
        """on new highscores update DB and UI"""
        if level > self.highscore:
            self.highscore_db.update_highscore(level)
            self.highscore = level
            self._turtle.clear()
            self.render_highscore()

    def render_highscore(self) -> None:
        """render the current level to the UI"""
        highscore: str = f"Highscore {self.highscore}"
        self._turtle.write(highscore, align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, "normal"))
