import pygame
import random
import numpy as np
from base import BaseEnv
from othello_objects2 import Cell


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
        self.turn_count = 64
        self.max_turn = self.cell_line ** 2 - 4
        self.is_black_turn = True
        self.width = width
        self.height = height
        self.cell_size = (width // self.cell_line, height // self.cell_line)
        self.around_changed = np.zeros(8, dtype=np.int8)

        self.put_cell = None
        self.black_putable = set()
        self.white_putable = set()

        background = pygame.image.load("./Othello/data/background.png")
        sprite_white = pygame.image.load("./Othello/data/othello_stone_white.png")
        sprite_blakc = pygame.image.load("./Othello/data/othello_stone_black.png")
        back_stone = pygame.image.load("./Othello/data/othello_stone_background.png")
        self.sprite_0 = pygame.image.load("./Othello/data/red.png")
        self.sprite_1 = pygame.image.load("./Othello/data/green.png")
        self.sprite_2 = pygame.image.load("./Othello/data/yellow.png")

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
            self.back_stone = back_stone
            self.background = background
            self.previous_time = 0.0
            self.framerate = 0.05

        half = self.cell_size[0] // 2 - 5
        self.info_offsets = (
            (0, 0),
            (half, 0),
            (half * 2, 0),
            (0, half),
            (half * 2, half),
            (0, half * 2),
            (half, half * 2),
            (half * 2, half * 2),
        )

    def reset(self):
        self.turn_count = 0
        self.is_black_turn = True
        self.black_putable.clear()
        self.white_putable.clear()

        for cols in self.cells:
            for cell in cols:
                cell.is_empty = True
                cell.around_black.all = 0
                cell.around_white.all = 0

        if self.enable_render:
            self.draw_grid()

        self.put((3, 3), False)
        self.put((4, 4), False)
        self.put((3, 4), True)
        self.put((4, 3), True)

        # self.state.fill(0)
        # self.state[3, 3] = 1
        # self.state[4, 4] = 1
        # self.state[3, 4] = -1
        # self.state[4, 3] = -1
        # return np.copy(self.state).reshape([1, 1, 8, 8])

    def step(self, action):
        return super().step(action)

    def close(self):
        pygame.quit()

    def change_color_to_direction(self, cell: Cell, to_black, to_dir):
        if cell.is_black == to_black:
            return 0

        self.set_color(cell, to_black)

        next_cell = cell.around_cells[to_dir]
        return self.change_color_to_direction(next_cell, to_black, to_dir) + 1

    def set_color(self, cell: Cell, to_black):
        cell.is_black = to_black
        cell.is_empty = False
        self.draw_cell(cell, to_black)

        for dir in range(4):
            dir_r = 7 - dir
            r_cell: Cell = cell.around_cells[dir]
            if r_cell and r_cell.is_empty == False:
                if r_cell.is_black != cell.is_black:
                    # cell.around_infos.dir[dir] = 2 if cell.is_black else 1
                    cell.set_direction_info(dir)
                else:
                    # cell.copy_direction_info(dir, r_cell)
                    cell.copy_direction_info(dir, r_cell)
            l_cell: Cell = cell.around_cells[dir_r]
            if l_cell and l_cell.is_empty == False:
                if l_cell.is_black != cell.is_black:
                    # cell.around_infos.dir[dir_r] = 2 if cell.is_black else 1
                    cell.set_direction_info(dir_r)
                else:
                    # cell.around_infos.dir[dir_r] = l_cell.around_infos.dir[dir_r]
                    cell.copy_direction_info(dir_r, l_cell)

            # self.draw_cell_info(cell, dir)
            # self.draw_cell_info(cell, dir_r)
            self.update_to_direction(r_cell, cell, dir)
            self.update_to_direction(l_cell, cell, dir_r)

    def update_to_direction(self, cell: Cell, before_cell: Cell, dir):
        if cell == None:
            return
        dir_r = 7 - dir
        if cell.is_empty:
            # cell.around_infos.dir[dir_r] = before_cell.around_infos.dir[dir_r]
            putable_black = cell.around_black.all != 0
            putable_white = cell.around_white.all != 0
            cell.copy_direction_info(dir_r, before_cell)
            if self.put_cell != cell:
                if putable_black != (cell.around_black.all != 0):
                    if putable_black:
                        self.black_putable.remove(cell)
                    else:
                        self.black_putable.add(cell)
                if putable_white != (cell.around_white.all != 0):
                    if putable_white:
                        self.white_putable.remove(cell)
                    else:
                        self.white_putable.add(cell)
            # self.draw_cell_info(cell, dir_r)
        elif before_cell.is_black == cell.is_black:
            # cell.around_infos.dir[dir_r] = before_cell.around_infos.dir[dir_r]
            cell.copy_direction_info(dir_r, before_cell)
            # self.draw_cell_info(cell, dir_r)
            self.update_to_direction(cell.around_cells[dir], cell, dir)
        else:
            # info = 2 if cell.is_black else 1
            # if info != cell.around_infos.dir[dir_r]:
            around_info = cell.around_white if cell.is_black else cell.around_black
            # if around_info & (1 << dir_r) == 0:
            if around_info.bit[dir_r] == False:
                # cell.around_infos.dir[dir_r] = info
                cell.set_direction_info(dir_r)
                # self.draw_cell_info(cell, dir_r)
                self.update_to_direction(cell.around_cells[dir], cell, dir)

    def put_to_cell(self, cell: Cell, to_black, remove_putable=True):
        if cell.is_empty == False:
            return 0

        self.turn_count += 1

        if remove_putable:
            if to_black:
                self.black_putable.remove(cell)
                if cell.around_white.all != 0:
                    self.white_putable.remove(cell)
            else:
                self.white_putable.remove(cell)
                if cell.around_black.all != 0:
                    self.black_putable.remove(cell)
            self.put_cell = cell

        around_info = cell.around_black if to_black else cell.around_white
        count = 0
        for to_dir in range(8):
            # if around_info & (1 << to_dir):
            if around_info.bit[to_dir]:
                next_cell = cell.around_cells[to_dir]
                count += self.change_color_to_direction(next_cell, to_black, to_dir)

        self.set_color(cell, to_black)
        return count

    def put(self, put_pos, to_black):
        cell = self.cells[put_pos[0]][put_pos[1]]
        self.put_to_cell(cell, to_black, False)

    def put_click_pos(self, pos):
        if pos == None:
            return
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.width or pos[1] > self.height:
            return

        put_pos = (int(pos[0] / self.cell_size[0]), int(pos[1] / self.cell_size[1]))
        cell = self.cells[put_pos[0]][put_pos[1]]
        if self.put_to_cell(cell , self.is_black_turn, True) > 0:
            self.is_black_turn = not self.is_black_turn
        else:
            self.reset()

    def put_random_cell(self):
        putable_list = self.black_putable if self.is_black_turn else self.white_putable
        if len(putable_list):
            cell = random.sample(putable_list, 1)[0]
            if self.put_to_cell(cell, self.is_black_turn, True) > 0:
                self.is_black_turn = not self.is_black_turn
                return
            else:
                raise Exception()
        self.reset()

    def draw_grid(self):
        self.window.blit(self.background, (0, 0))
        for x in range(0, self.width, self.cell_size[0]):
            pygame.draw.line(self.window, (0, 0, 0, 50), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size[1]):
            pygame.draw.line(self.window, (0, 0, 0, 50), (0, y), (self.width, y))

    def draw_cell(self, cell: Cell, to_black):
        if self.enable_render == False:
            return
        if to_black:
            self.window.blit(self.sprite_blakc, cell.pos * self.cell_size)
        else:
            self.window.blit(self.sprite_white, cell.pos * self.cell_size)

    def draw_cell_info(self, cell: Cell, dir):
        # if cell.around_black & (1 << dir):
        if cell.around_black.bit[dir]:
            sprite = self.sprite_1
        # elif cell.around_white & (1 << dir):
        elif cell.around_white.bit[dir]:
            sprite = self.sprite_2
        else:
            sprite = self.sprite_0
        self.window.blit(sprite, cell.pos * self.cell_size + self.info_offsets[dir])
