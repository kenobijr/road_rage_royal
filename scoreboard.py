from turtle import Turtle

TEXT_ALIGNMENT: str = "left"
FONT_TYPE: str = "Courier"
FONT_STYLE: str = "bold"
FONT_SIZE: int = 30


class Scoreboard(Turtle):
    """manage the scoreboard logic and game over message"""
    def __init__(self) -> None:
        super().__init__()
        self.level: int = 1
        self.penup()
        self.hideturtle()
        self.goto(-287, 257)
        self.render_level()

    def render_level(self) -> None:
        """render the current level to the UI"""
        level: str = f"Level: {self.level}"
        self.write(level, align=TEXT_ALIGNMENT, font=(FONT_TYPE, FONT_SIZE, FONT_STYLE))

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

    def game_over(self) -> None:
        """show big game over message in center of UI"""
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=(FONT_TYPE, 50, FONT_STYLE))
