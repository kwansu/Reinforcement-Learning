import pygame
import random
import numpy as np
from base import BaseEnv
from othello_objects import Cell


class Othello(BaseEnv):
    def __init__(self, width, height, render):
        line_count = 8
        self.enable_render = render
        self.state_size = [1, line_count, line_count]
        self.action_size = line_count * line_count
        self.action_type = "discrete"
        self.score = 0

        self.state = np.zeros([line_count, line_count], dtype=np.int8)
        self.cell_line = line_count
        self.turn_count = 0
        self.max_turn = self.cell_line ** 2 - 4
        self.is_black_turn = True
        self.width = width
        self.height = height
        self.cell_size = (width // self.cell_line, height // self.cell_line)
        self.around_changed = np.zeros(8, dtype=np.int8)

        self.black_putable_list = []
        self.white_putable_list = []

        background = pygame.image.load("./Othello/data/background.png")
        sprite_white = pygame.image.load("./Othello/data/othello_stone_white.png")
        sprite_blakc = pygame.image.load("./Othello/data/othello_stone_black.png")
        sprite_putable_black = pygame.image.load("./Othello/data/othello_stone_putable_black.png")
        sprite_putable_white = pygame.image.load("./Othello/data/othello_stone_putable_white.png")
        back_stone = pygame.image.load("./Othello/data/othello_stone_background.png")

        self.cells = tuple(
            tuple(Cell((col, row)) for row in range(self.cell_line))
            for col in range(self.cell_line)
        )

        for colums in self.cells:
            for cell in colums:
                cell.set_around_cells(self.cells)

        if self.enable_render:
            pygame.init()
            self.window = pygame.display.set_mode((width, height))

            self.sprite_white = sprite_white
            self.sprite_blakc = sprite_blakc
            self.sprite_putable_black = sprite_putable_black
            self.sprite_putable_white = sprite_putable_white
            self.back_stone = back_stone
            self.background = background
            self.previous_time = 0.0
            self.framerate = 0.05

    def close(self):
        pygame.quit()

    def put(self, pos, to_black):
        cell: Cell = self.cells[pos[0]][pos[1]]

        if cell.is_empty == False:
            return 0

        cell.set_color(to_black)
        changed_count = 0
        for to_dir in range(8):
            next_cell = cell.around_cells[to_dir]
            changed_count += self.change_color_to_direction(next_cell, to_black, to_dir)

        return changed_count

    def change_color_to_direction(self, cell: Cell, to_black, to_dir):
        if cell == None or cell.is_empty or cell.is_black == to_black:
            return 0

        cell.set_color(to_black)

        next_cell = cell.around_cells[to_dir]
        return self.change_color_to_direction(next_cell, to_black, to_dir) + 1
