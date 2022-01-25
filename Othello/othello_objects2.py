import numpy as np
from ctypes import *


class Cell:
    class around_info(Union):
        _fields_ = [("dir", c_bool * 8), ("putable", c_longlong)]

    def __init__(self, pos=(-1, -1)):
        self.pos = np.array(pos)
        self.is_empty = True
        self.is_black = False
        self.putable_black = False
        self.putable_white = False
        self.around_cells = [None for i in range(8)]
        self.around_black = self.around_info()
        self.around_white = self.around_info()

    def update_putable(self, before_black):
        pass

    def set_enable_direction_info(self, dir, is_black):
        if is_black:
            self.around_black.dir[dir] = True
            self.around_white.dir[dir] = False
        else:
            self.around_black.dir[dir] = False
            self.around_white.dir[dir] = True

    def set_direction_info(self, dir):
        if self.is_black:
            self.around_black.dir[dir] = False
            self.around_white.dir[dir] = True
        else:
            self.around_black.dir[dir] = True
            self.around_white.dir[dir] = False

    def copy_direction_info(self, dir, cell):
        self.around_black.dir[dir] = cell.around_black.dir[dir]
        self.around_white.dir[dir] = cell.around_white.dir[dir]

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
