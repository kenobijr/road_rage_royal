from turtle import Screen, Turtle
from typing import Optional, Dict

# custom shapes for turtle objects need to be registered to the screen
SHAPE_PATHS = [
    "assets/car.gif",
    "assets/explosion.gif"
]

TEXT_ALIGNMENT: str = "left"
FONT_TYPE: str = "Courier"
FONT_STYLE: str = "normal"


class GameScreen:
    """
    - sets up the screen and writes instructions onto it using turtle objects
    - disables automatic screen update, meaning graphics will not be updated in real-time
    - instead screen.update() is used manually within the game loop to refresh the screen and control game speed
    - x - y coordinate system -> when full width = 600, foremost left x-coordinate is -300, foremost right is 300
    boundaries:
    - top: drawn threshold under screen top border; player teleports to bottom when crossing it; no cars appear above
    - bottom: drawn threshold above screen bottom; player cannot move down before crossing it; no cars appear below
    - left: player can't cross it; cars are wrecked when crossing it; added 2px space by testing for player shape
    - right: player can't cross it; cars are generated beyond it; added 2px space by testing for player shape
    """
    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        title: str = "ROAD RAGE ROYAL"
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.top_boundary: int = int((self.height / 2) - 50)
        self.bottom_boundary: int = int(-(self.height / 2) + 60)
        self.left_boundary: int = int(-(self.width / 2)) + 2
        self.right_boundary: int = int(self.width / 2) - 4
        # add Screen object
        self._turtle_screen = Screen()
        self._turtle_screen.setup(width=width, height=height)
        self._turtle_screen.title(title)
        # disables automatic screen updates
        self._turtle_screen.tracer(0)
        # register custom screens
        self.add_shapes(SHAPE_PATHS)
        # add turtle object to draw lines & add texts
        self._turtle_helper = Turtle()
        self._turtle_helper.hideturtle()
        # draw lines with helper turtle
        self.draw_lines()
        # write descriptions with helper turtle
        self.write_descriptions()
        # mark helper for gc
        self._turtle_helper = None

    def add_shapes(self, custom_shapes: list[str]) -> None:
        for shape in custom_shapes:
            self._turtle_screen.register_shape(shape)

    def draw_lines(self):
        # draw start line at bottom boundary
        self._turtle_helper.teleport(self.left_boundary, self.bottom_boundary)
        self._turtle_helper.goto(self.right_boundary, self.bottom_boundary)
        # draw finish line at top boundary
        self._turtle_helper.teleport(self.left_boundary, self.top_boundary)
        self._turtle_helper.goto(self.right_boundary, self.top_boundary)
        # put pen up when drawing is finished
        self._turtle_helper.penup()

    def write_descriptions(self):
        # teleport and write text "safe zone" within the starting area
        self._turtle_helper.teleport(150, -280)
        self._turtle_helper.write("SAFE ZONE", align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, FONT_STYLE))
        # teleport and write text "cross line to teleport" within the finish area
        self._turtle_helper.teleport(120, 260)
        self._turtle_helper.write("TARGET AREA", align=TEXT_ALIGNMENT, font=(FONT_TYPE, 25, FONT_STYLE))

    def attach_event_listeners(self, bindings: Dict) -> None:
        """adds and activates event listeners for player movement"""
        self._turtle_screen.listen()
        for key, action in bindings.items():
            self._turtle_screen.onkey(action, key)

    def update_screen(self) -> None:
        """since auto screen update is deactivated by .tracer(0) in init, screen needs to be updated manually"""
        self._turtle_screen.update()

    def show_prompt(self, headline: str, prompt: str) -> Optional[str]:
        """shows input with headline and prompt on screen; returns received answer as str or None if canceled"""
        return self._turtle_screen.textinput(headline, prompt)
