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
        self.around_counts = np.zeros(8, dtype=np.int32)

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

    def reset(self):
        self.turn_count = 0
        self.is_black_turn = True
        self.black_putable_list.clear()
        self.white_putable_list.clear()

        for cols in self.cells:
            for cell in cols:
                cell.is_empty = True
                cell.bit_around_black = 0
                cell.bit_around_white = 0

        if self.enable_render:
            self.draw_grid()

        self.put((3, 3), False)
        self.put((4, 4), False)
        self.put((3, 4), True)
        self.put((4, 3), True)

        self.state.fill(0)
        self.state[3, 3] = 1
        self.state[4, 4] = 1
        self.state[3, 4] = -1
        self.state[4, 3] = -1
        return np.copy(self.state).reshape([1, 1, 8, 8])

    def render(self):
        for event in pygame.event.get():
            pass
        pygame.display.update()

    def draw_grid(self):
        self.window.blit(self.background, (0, 0))
        for x in range(0, self.width, self.cell_size[0]):
            pygame.draw.line(self.window, (0, 0, 0, 50), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size[1]):
            pygame.draw.line(self.window, (0, 0, 0, 50), (0, y), (self.width, y))

    def draw_cell(self, cell: Cell, to_black):
        cell.is_black = to_black

        if self.enable_render == False:
            return
        if to_black:
            self.window.blit(self.sprite_blakc, cell.pos * self.cell_size)
        else:
            self.window.blit(self.sprite_white, cell.pos * self.cell_size)

    def put(self, pos, to_black):
        cell: Cell = self.cells[pos[0]][pos[1]]

        if cell.is_empty == False:
            return 0

        cell.is_empty = False
        self.draw_cell(cell, to_black)

        reward = 0
        for dir in range(0, 8):
            if cell.get_bit_around_putable() & 1 << dir != 0:
                reward += self.change_color(cell.around_cells[dir], dir, to_black)

        cell.bit_around_black = 0
        cell.bit_around_white = 0
        self.update_putable_list(cell)
        self.remove_putable_list(cell)
        return reward

    def add_putable_direction(self, cell: Cell, dir):
        dir_r = 7 - dir
        if cell.get_bit_around_putable() & 1 << dir_r == 0:
            cell.add_putable_direction(dir_r, cell.is_black)
            next_cell: Cell = cell.around_cells[dir]
            if next_cell == None:
                return
            if next_cell.is_empty:
                next_cell.add_putable_direction(dir_r, not cell.is_black)
                self.remove_putablelist_color(next_cell, cell.is_black)
                self.add_putable_list(next_cell, not cell.is_black)
            elif next_cell.is_black == cell.is_black:
                self.add_putable_direction(next_cell, dir)

    def remove_putable_direction(self, cell: Cell, dir):
        dir_r = 7 - dir
        if cell.get_bit_around_putable() & 1 << dir_r != 0:
            cell.remove_putable_direction(dir_r)
            next_cell: Cell = cell.around_cells[dir]
            if next_cell == None:
                return
            if next_cell.is_empty:
                next_cell.remove_putable_direction(dir_r)
                self.remove_putablelist_color(next_cell, not cell.is_black)
            elif next_cell.is_black == cell.is_black:
                self.remove_putable_direction(next_cell, dir)

    def update_putable_list(self, cell: Cell):
        for dir in range(8):
            dir_r = 7 - dir
            next_cell: Cell = cell.around_cells[dir]
            if next_cell == None:
                continue
            if next_cell.is_empty:
                if cell.get_bit_around_putable() & 1 << dir_r != 0:
                    next_cell.add_putable_direction(dir_r, not cell.is_black)
                    self.add_putable_list(next_cell, not cell.is_black)
                    if next_cell.get_bit_around_putable_color(cell.is_black) == 0:
                        self.remove_putablelist_color(next_cell, cell.is_black)
                else:
                    next_cell.remove_putable_direction(dir_r)
                    self.remove_putablelist_color(next_cell, cell.is_black)
            elif next_cell.is_black == cell.is_black:
                if next_cell.get_bit_around_putable() & 1 << dir != 0:
                    self.add_putable_direction(cell, dir_r)
                if cell.get_bit_around_putable() & 1 << dir_r == 0:
                    self.remove_putable_direction(next_cell, dir)
            else:
                self.add_putable_direction(next_cell, dir)
                self.add_putable_direction(cell, dir_r)

    def add_putable_list(self, cell: Cell, to_black):
        putable_list = self.black_putable_list if to_black else self.white_putable_list
        if cell in putable_list:
            return
        putable_list.append(cell)
        # if cell.is_empty and not to_black:
        #     self.window.blit(self.sprite_yellow, cell.pos* self.cell_size)

    def remove_putablelist_color(self, cell: Cell, to_black):
        if cell.get_putable(not to_black):
            return
        putable_list = self.black_putable_list if to_black else self.white_putable_list
        if cell in putable_list:
            putable_list.remove(cell)
        # if not to_black and cell.is_empty:
        #     self.window.blit(self.back_stone, cell.pos* self.cell_size)

    def remove_putable_list(self, cell: Cell):
        if cell in self.black_putable_list:
            self.black_putable_list.remove(cell)
        if cell in self.white_putable_list:
            self.white_putable_list.remove(cell)

    def change_color(self, cell: Cell, dir, to_black):
        self.state[cell.pos[0], cell.pos[1]] = 1 if to_black else -1
        cell.bit_around_black = 0
        cell.bit_around_white = 0
        self.draw_cell(cell, to_black)
        self.update_putable_list(cell)
        next_cell: Cell = cell.around_cells[dir]
        if next_cell.is_black != to_black:
            return self.change_color(next_cell, dir, to_black) + 1
        return 1

    def put_cell(self, put_pos):
        reward = self.put2(put_pos, self.is_black_turn)
        if reward <= 0:
            self.reset()
            return

        self.is_black_turn = not self.is_black_turn
        putable_list = (
            self.black_putable_list if self.is_black_turn else self.white_putable_list
        )
        if len(putable_list) == 0:
            self.reset()
            return
