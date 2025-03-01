import pytest
# from turtle import Screen
from screen import GameScreen


def test_GameScreen_init_attributes():
    """test initiation instance params of screen object"""
    screen = GameScreen()
    assert screen.width == 600
    assert screen.height == 600
    assert screen.title == "ROAD RAGE ROYAL"
    assert screen.top_boundary == 250
    assert screen.bottom_boundary == -240
    assert screen.left_boundary == -298
    assert screen.right_boundary == 296


def test_GameScreen_init_screen_obj():
    """test initiation of screen obj saved as class attribute"""
    screen = GameScreen()
    assert hasattr(screen, "_turtle_screen")
    assert screen._turtle_screen.window_width() == 600
    assert screen._turtle_screen.window_height() == 600
    assert screen._turtle_screen.tracer() == 0


def test_GameScreen_add_shapes():
    """by initiating object "car.gif" and "explosion.gif" must be added as custom shaped"""
    screen = GameScreen()
    registered_shapes = screen._turtle_screen.getshapes()
    assert "car.gif" in registered_shapes
    assert "explosion.gif" in registered_shapes
