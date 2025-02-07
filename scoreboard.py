from turtle import Turtle
from highscore_db import HighscoreDB

TEXT_ALIGNMENT: str = "left"
FONT_TYPE: str = "Courier"


class Scoreboard(Turtle):
    """manage the scoreboard logic showing the level of the current game"""
    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__()
        self.level: int = 1
        self.penup()
        self.hideturtle()
        self.goto(start_x, start_y)
        self.render_level()

    def render_level(self) -> None:
        """render the current level to the UI"""
        level: str = f"Level {self.level}"
        self.write(level, align=TEXT_ALIGNMENT, font=(FONT_TYPE, 30, "bold"))

    def increase_level(self) -> None:
        """update level counter, clear UI and trigger render_level"""
        self.level += 1
        self.clear()
        self.render_level()

    def reset_level(self) -> None:
        """reset level after game restart"""
        self.level: int = 1
        self.clear()
        self.render_level()


class Highscore(Turtle):
    """manages the highscore logic showing and updating the highscore over all games played using sqlite3 DB"""
    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__()
        # initiate & set up sqlite3 DB initially with default value 1 if not already existing
        self.highscore_db = HighscoreDB()
        # reads highscore from DB
        self.highscore = self.highscore_db.read_db()
        self.penup()
        self.hideturtle()
        self.goto(start_x, start_y)
        self.render_highscore()

    def update_highscore(self, level):
        """read highscore from DB; if necessary update it in DB and UI"""
        self.highscore = self.highscore_db.read_db()
        if level > self.highscore:
            self.highscore_db.update_highscore(level)
            self.highscore = level
            self.clear()
            self.render_highscore()

    def render_highscore(self) -> None:
        """render the current level to the UI"""
        highscore: str = f"Highscore {self.highscore}"
        self.write(highscore, align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, "normal"))
