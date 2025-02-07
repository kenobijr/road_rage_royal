# importing the module single to be able to change color mode on module level to rgb
import turtle
from turtle import Turtle
from helpers import random_color, create_block_batch
from screen import SCREEN_WIDTH
from typing import List, Tuple
# change color mode on module level
turtle.colormode(255)


class BlockManager:
    """
    - core game logic creating blocks, steering and removing them
    - game iterations are dictated by screen updating, steered by the self.speed variable setting value for time.sleep
    - every game iteration it is checked, if a new batch of blocks is generated
    - a batch of blocks is distributed non-overlapping along the y-axis with identical x-coordinate
    - multiple batches have a min. distance non-overlapping between them along the x-axis
    - block batches are generated at a defined genesis point at right side out of screen running from right to left
    - block batches going over the screen on the left side are wrecked
    - on level up difficulty increased by changing self.speed and self.block_batch_max
    """
    def __init__(self) -> None:
        self.block_container: List[Turtle] = []
        # value for time.sleep in main game loop dictating game speed
        self.speed: float = 0.2
        # distance in px of every block moving forward one time
        self.move_distance: int = 5
        # value for upper boundary of new generated block batch; increases with game difficulty
        self.block_batch_max: int = 3
        # value for bottom boundary of new generated block batch; increases with game difficulty
        self.block_batch_min: int = 0
        # gap in px along x-axis between block batches
        self.block_batch_x_gap: float = 80
        # gap in px along y-axis between single block within a batch
        self.block_batch_y_gap: float = 25
        # genesis x cor for new block batches; beyond the screen on the right side
        self.x_genesis_cor: int = int((SCREEN_WIDTH / 2) + 20)
        # block going beyond this x cor (out of screen) are wrecked
        self.x_wrecking_cor: int = int(-(SCREEN_WIDTH / 2) - 20)
        # add first batch of blocks on initiating blocks manager
        self.add_blocks()

    def add_blocks(self) -> None:
        """
        - determines if a new block_batch is added dependent of the state of the existing blocks
        - if no blocks exist at game start, a new batch is always created
        - if at least one block batch exists, the distance of the rightmost block batch x-coordinate is checked
        - if this distance / gap is big enough, the creation of a further block batch is triggered
        - this way the overlapping of blocks along the x-axis is prevented
        """
        # for empty block_container create new batch always
        if not self.block_container:
            block_batch: List[Tuple[int, int]] = create_block_batch(
                self.block_batch_min,
                self.block_batch_max,
                self.block_batch_y_gap,
                self.x_genesis_cor
            )
            self.render_blocks(block_batch)
        else:
            # determine x-coordinate of rightmost block
            rightmost_x: float = max(car.xcor() for car in self.block_container)
            # only add blocks after min gap on x-axis
            if rightmost_x < self.x_genesis_cor - self.block_batch_x_gap:
                block_batch: List[Tuple[int, int]] = create_block_batch(
                    self.block_batch_min,
                    self.block_batch_max,
                    self.block_batch_y_gap,
                    self.x_genesis_cor)
                self.render_blocks(block_batch)

    def render_blocks(self, block_coordinates: List[Tuple[int, int]]) -> None:
        """
        - takes list of tuple block-coordinates as input
        - creates blocks as turtle objects for each tuple
        - appends each block to self.block_container
        """
        for block in block_coordinates:
            new_block: Turtle = Turtle("square")
            new_block.penup()
            # stretch it to size 40x20 px as rectangle
            new_block.shapesize(stretch_wid=1, stretch_len=2)
            # retrieving random rgb colors from helpers.py
            new_block.color(random_color())
            new_block.goto(block[0], block[1])
            self.block_container.append(new_block)

    def move_blocks(self) -> None:
        """
        - move all blocks in the car_container forward by reducing the x-coordinate
        - determined by move_distance and self.speed
        """
        for block in self.block_container:
            new_x: float = block.xcor() - self.move_distance
            block.goto(new_x, block.ycor())

    def wreck_blocks(self) -> None:
        """
        - delete all blocks crossing the left screen border
        - determined by the x-wrecking-coordinate as boundary
        """
        # Iterate through blocks and clean up those that need to be wrecked
        for block in self.block_container:
            # check if blocks need to be wrecked due to crossing the left screen border
            if block.xcor() < self.x_wrecking_cor:
                block.hideturtle()
                block.clear()
        # filter out blocks that are wrecked and rebuild the container
        self.block_container = [block for block in self.block_container if block.xcor() >= self.x_wrecking_cor]

    def reset(self) -> None:
        """ delete all blocks and reset difficulty for game restart"""
        for block in self.block_container:
            block.hideturtle()
            block.clear()
        self.block_container.clear()
        self.block_batch_max = 3
        self.block_batch_min = 0
        self.speed = 0.2

    def increase_difficulty(self, level) -> None:
        """ increase game difficulty when player levels up for delivered level"""
        self.speed *= 0.95
        if level >= 3:
            self.block_batch_max += 1
        if level >= 5:
            self.block_batch_x_gap *= 0.95
            self.block_batch_y_gap *= 0.95
        if level >= 7:
            self.block_batch_min += 1

    def update_blocks(self) -> None:
        """ wrapper for move, add and wreck blocks"""
        self.move_blocks()
        self.add_blocks()
        self.wreck_blocks()
