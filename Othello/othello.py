import time
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

        self.state = np.zeros([8, 8], dtype=np.int8)
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

    def step(self, action_pos):
        self.turn_count += 1
        action_pos = divmod(action_pos.max(), 8)  # self.cell_line)
        is_termimal = False

        reward = self.put(action_pos, self.is_black_turn)
        if reward <= 0:
            reward -= 50
            is_termimal = True
        else:
            if self.enable_render:
                self.render()

            self.state[action_pos[0], action_pos[1]] = 1 if self.is_black_turn else -1
            self.is_black_turn = not self.is_black_turn

            assert not self.is_black_turn
            is_termimal = self.put_random_cell()

            if self.turn_count >= self.max_turn:
                black_count, white_count = self.calculate_count()
                if black_count > white_count:
                    reward += 50
                is_termimal = True

        reward = np.expand_dims([reward], 0)
        is_termimal = np.expand_dims([is_termimal], 0)
        return (np.copy(self.state).reshape([1, 1, 8, 8]), reward, is_termimal)

    def render(self):
        for event in pygame.event.get():
            pass
        # if pygame.display.get_active():
        #     cur_time = time.time()
        #     if cur_time - self.previous_time >= self.framerate:
        #         self.previous_time = cur_time
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

    def draw_putable_cell(self, cell: Cell):
        if cell.is_empty == False:
            return
        
        self.window.blit(self.back_stone, cell.pos * self.cell_size)
        if cell.get_putable(True):
            self.window.blit(self.sprite_putable_black, cell.pos * self.cell_size)
        if cell.get_putable(False):
            self.window.blit(self.sprite_putable_white, cell.pos * self.cell_size)

    def put(self, pos, to_black):
        cell: Cell = self.cells[pos[0]][pos[1]]

        if cell.is_empty == False:
            return 0

        cell.is_empty = False
        self.draw_cell(cell, to_black)
        # bit_around_putable = cell.bit_around_black if to_black else cell.bitAroundPutableWhite
        # putable_list = self.black_putable_list bit_around_white to_black else self.white_putable_list

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

    def calculate_count(self):
        black_count = 0
        white_count = 0
        for cols in self.cells:
            for cell in cols:
                if cell.is_empty == False:
                    if cell.is_black:
                        black_count += 1
                    else:
                        white_count += 1

        return black_count, white_count

    def get_put_randomable_pos(self):
        putable_list = (
            self.black_putable_list if self.is_black_turn else self.white_putable_list
        )
        return random.choice(putable_list).pos

    def put_random_cell(self):
        self.turn_count += 1
        reward = 0
        putable_list = (
            self.black_putable_list if self.is_black_turn else self.white_putable_list
        )

        # if len(putable_list) == 0:
        #     self.reset()
        #     return
        if putable_list:
            random_cell = random.choice(putable_list)
            reward = self.put(random_cell.pos, self.is_black_turn)
        # if reward <= 0:
        #     self.reset()
        #     return

        self.is_black_turn = not self.is_black_turn
        return reward <= 0

    def put_cell(self, put_pos):
        reward = self.put(put_pos, self.is_black_turn)
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

    def put_click_pos(self, pos):
        # self.turn_count+=1
        if pos == None:
            return
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.width or pos[1] > self.height:
            return

        put_pos = (int(pos[0] / self.cell_size[0]), int(pos[1] / self.cell_size[1]))
        self.put_cell(put_pos)

    def _change_color2(self, cell: Cell, to_black, to_dir, count=0):
        if cell.is_black == to_black:
            return count

        next_cell: Cell = cell.around_cells[to_dir]
        if next_cell == None or next_cell.is_empty:
            return 0

        result = self._change_color2(next_cell, to_black, to_dir, count + 1)
        if result > 0:
            self.draw_cell(cell, to_black)
        return result

    def _update_putable_list2(self, cell: Cell, to_black, dir):
        if to_black:
            putable_list = self.black_putable_list
            putable_list_r = self.white_putable_list
        else:
            putable_list = self.white_putable_list
            putable_list_r = self.black_putable_list

        before_r = cell.get_putable(not to_black)
        before = cell.get_putable(to_black)

        cell.add_putable_direction(dir, to_black)
        if before == False:
            assert cell not in putable_list
            putable_list.append(cell)
            self.draw_putable_cell(cell)

        if before_r and cell.get_putable(not to_black) == False:
            putable_list_r.remove(cell)
            self.draw_putable_cell(cell)

    def _check_putable(self, cell: Cell, to_black, to_dir):
        if cell.is_black == to_black:
            return True

        next_cell: Cell = cell.around_cells[to_dir]
        if next_cell == None or next_cell.is_empty:
            return False

        return self._check_putable(next_cell, to_black, to_dir)

    def _remove_putable_direction2(self, cell: Cell, to_black, dir):
        if cell.get_putable(to_black):
            cell.remove_putable_direction(dir)
            if cell.get_putable(to_black) == False:
                t = self.black_putable_list if to_black else self.white_putable_list
                t.remove(cell)
                self.draw_putable_cell(cell)

    def _update_putable_direction(self, cell: Cell, to_black, dir):
        dir_r = 7 - dir
        next_cell: Cell = cell.around_cells[dir]
        if next_cell == None or next_cell.is_empty == False:
            return
        next_cell_r: Cell = cell.around_cells[dir_r]
        if next_cell_r == None or next_cell_r.is_empty:
            return

        if self._check_putable(next_cell, to_black, dir):
            self._update_putable_list2(next_cell, to_black, dir_r)
        else:
            self._remove_putable_direction2(next_cell, not to_black, dir_r)

    def _update_around(self, cell: Cell, to_black, to_dir, count):
        assert cell.is_empty == False and cell.is_black != to_black
        if count <= 0:
            return

        to_dir_r = 7 - to_dir
        for dir in range(8):
            if dir == to_dir or dir == to_dir_r:
                continue
            self._update_putable_direction(cell, to_black, dir)

        self._update_around(cell.around_cells[to_dir], to_black, dir, count - 1)

    def put2(self, pos, to_black):
        cell: Cell = self.cells[pos[0]][pos[1]]

        if cell.is_empty == False:
            return 0

        cell.is_empty = False
        self.draw_cell(cell, to_black)

        reward = 0
        for dir in range(8):
            next_cell = cell.around_cells[dir]
            if next_cell and next_cell.is_empty == False:
                count = self._change_color2(next_cell, to_black, dir)
                reward += count
                self.around_counts[dir] = count
            else:
                self.around_counts[dir] = 0

        # if reward == 0:
        #     return 0

        for dir in range(8):
            next_cell: Cell = cell.around_cells[dir]
            count = self.around_counts[dir]
            if count > 0:
                self._update_around(next_cell, not to_black, dir, count)
            elif next_cell and next_cell.is_empty:
                self._update_putable_direction(cell, not to_black, dir)

        self.state
        
        return reward
