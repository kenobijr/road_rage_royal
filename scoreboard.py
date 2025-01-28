from turtle import Turtle

TEXT_ALIGNMENT = "left"
FONT_TYPE = "Courier"
FONT_STYLE = "bold"
FONT_SIZE = 30


class Scoreboard(Turtle):
    """manage all game board logic and game over message"""
    def __init__(self):
        super().__init__()
        self.level = 1
        self.penup()
        self.hideturtle()
        self.goto(-287, 257)
        self.render_level()

    def render_level(self):
        score_str = f"Level: {self.level}"
        self.write(score_str, align=TEXT_ALIGNMENT, font=(FONT_TYPE, FONT_SIZE, FONT_STYLE))

    def increase_level(self):
        self.level += 1
        self.clear()
        self.render_level()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=(FONT_TYPE, 50, FONT_STYLE))
