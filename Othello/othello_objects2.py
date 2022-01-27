import numpy as np
from ctypes import *


class Cell:
    class AroundUnion(Union):
        _fields_ = [("bit", c_bool * 8), ("all", c_int64)]

    def __init__(self, pos=(-1, -1)):
        self.pos = np.array(pos)
        self.is_empty = True
        self.is_black = False
        self.around_cells = [None for i in range(8)]
        self.around_black = self.AroundUnion()
        self.around_white = self.AroundUnion()

    def set_direction_info(self, dir):
        # bit_info = 1 << dir
        # if self.is_black:
        #     self.around_black &= ~bit_info
        #     self.around_white |= bit_info
        # else:
        #     self.around_black |= bit_info
        #     self.around_white &= ~bit_info
        if self.is_black:
            self.around_black.bit[dir] = False
            self.around_white.bit[dir] = True
        else:
            self.around_black.bit[dir] = True
            self.around_white.bit[dir] = False

    def set_direction_info_color(self, dir, before_black):
        # bit_info = 1 << dir
        # if before_black:
        #     self.around_black &= ~bit_info
        #     self.around_white |= bit_info
        # else:
        #     self.around_black |= bit_info
        #     self.around_white &= ~bit_info
        if before_black:
            self.around_black.bit[dir] = False
            self.around_white.bit[dir] = True
        else:
            self.around_black.bit[dir] = True
            self.around_white.bit[dir] = False

    def copy_direction_info(self, dir, before_cell):
        # b = 1 << dir
        # self.around_black = (self.around_black & ~b) | (before_cell.around_black & b)
        # self.around_white = (self.around_white & ~b) | (before_cell.around_white & b)
        self.around_black.bit[dir] = before_cell.around_black.bit[dir]
        self.around_white.bit[dir] = before_cell.around_white.bit[dir]
        
    def set_around_cells(self, cells):
        self.__set_around_cell(self.pos[0] - 1, self.pos[1] - 1, cells, 0)
        self.__set_around_cell(self.pos[0], self.pos[1] - 1, cells, 1)
        self.__set_around_cell(self.pos[0] + 1, self.pos[1] - 1, cells, 2)
        self.__set_around_cell(self.pos[0] - 1, self.pos[1], cells, 3)
        self.__set_around_cell(self.pos[0] + 1, self.pos[1], cells, 4)
        self.__set_around_cell(self.pos[0] - 1, self.pos[1] + 1, cells, 5)
        self.__set_around_cell(self.pos[0], self.pos[1] + 1, cells, 6)
        self.__set_around_cell(self.pos[0] + 1, self.pos[1] + 1, cells, 7)

    def __set_around_cell(self, x, y, cells, dir):
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return
        self.around_cells[dir] = cells[x][y]
