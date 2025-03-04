from src.screen import GameScreen
from unittest.mock import patch


@patch("src.screen.Screen")
@patch("src.screen.Turtle")
def test_GameScreen_init_attributes(mock_screen_turtle_class, mock_screen_screen_class):
    """test initiation instance params of screen object; patched out to prevent GUI since no turtle states needed"""
    screen = GameScreen()
    assert screen.width == 600
    assert screen.height == 600
    assert screen.title == "ROAD RAGE ROYAL"
    assert screen.top_boundary == 250
    assert screen.bottom_boundary == -240
    assert screen.left_boundary == -298
    assert screen.right_boundary == 296

@patch("src.screen.Turtle")
def test_GameScreen_init_screen_obj(mock_screen_turtle_class):
    """test initiation of screen obj saved as class attribute; patched out helper_turtle since not needed"""
    screen = GameScreen()
    assert hasattr(screen, "_turtle_screen")
    assert screen._turtle_screen.window_width() == 600
    assert screen._turtle_screen.window_height() == 600
    assert screen._turtle_screen.tracer() == 0

@patch("src.screen.Turtle")
def test_GameScreen_add_shapes(mock_screen_turtle_class):
    """by initiating object "car.gif" and "explosion.gif" must be added as custom shape; patched out helper_turtle"""
    screen = GameScreen()
    registered_shapes = screen._turtle_screen.getshapes()
    assert "assets/car.gif" in registered_shapes
    assert "assets/explosion.gif" in registered_shapes
