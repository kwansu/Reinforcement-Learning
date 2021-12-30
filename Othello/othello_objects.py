import numpy as np


class Cell:
    def __init__(self, pos=(-1, -1)):
        self.pos = np.array(pos)
        self.is_empty = True
        self.is_black = False
        self.bit_around_black = 0  # 주변 8방향으로 둘 수 있는지를 비트 단위로 저장
        self.bit_around_white = 0
        self.around_cells = [None for i in range(8)]

    def get_putable(self, to_black):
        return self.bit_around_white if to_black else self.bit_around_black != 0

    def get_bit_around_putable(self):
        return self.bit_around_black if self.is_black else self.bit_around_white

    def get_bit_around_putable_color(self, is_black):
        return self.bit_around_white if is_black else self.bit_around_black

    def add_putable_direction(self, dir, is_black):
        bitInfo = 1 << dir
        if is_black:
            self.bit_around_black |= bitInfo
            self.bit_around_white &= ~bitInfo
        else:
            self.bit_around_white |= bitInfo
            self.bit_around_black &= ~bitInfo

    def remove_putable_direction(self, dir):
        bitInfo = 1 << dir
        self.bit_around_black &= ~bitInfo
        self.bit_around_white &= ~bitInfo

    # def change_color(self, to_black):
    #     self.is_black = to_black
    #     self.bit_around_black = 0
    #     self.bit_around_white = 0

    # #현재 셀에서 주위 8방향에 대해 둘 수 있는 경우를 추가함
    # #이미 추가되어있다면 false, 아니라면 true
    # def add_putable(self, bit_putable_info, is_black)->bool:
    #     if is_black:
    #         if bit_putable_info & self.bit_around_black == 0:
    #             self.bit_around_black+=bit_putable_info
    #             return True
    #     else:
    #         if bit_putable_info & self.bit_around_white == 0:
    #             self.bit_around_white+=bit_putable_info
    #             return True
    #     return False

    # #주위 8방향에 대해 더 이상 둘 수 있는 곳이 없으면 참, 아니면 거짓
    # #정확하게는 가능리스트에서 삭제해야할 경우만 참
    # def remove_putable(self, bit_putable_info, is_black) -> bool:
    #     if is_black:
    #         if self.bit_around_black & bit_putable_info != 0:
    #             self.bit_around_black -= bit_putable_info
    #             return True if self.bit_around_black == 0 else False
    #     else:
    #         if self.bit_around_white & bit_putable_info != 0:
    #             self.bit_around_white -= bit_putable_info
    #             return True if self.bit_around_white == 0 else False
    #     return False

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

    # UP_LEFT = 0b10
    # UP = 0b100
    # UP_RIGHT = 0b1000
    # LEFT = 0b10000
    # RIGHT = 0b100000
    # DOWN_LEFT = 0b1000000
    # DOWN_ = 0b10000000
    # DOWN_RIGHT = 0b100000000

    # PUT_IMPOSSIBLE = 0
    # PUT_CAN_BLACK = 1
    # PUT_CAN_WHITE = 2
    # PUT_OUT = 3

    # BIT_BLACK = 0b0001
    # BIT_WHITE = 0b0010
    # BIT_OUT = 0b0100
    # BIT_CHANGEABLE = 0b1000

    # BIT_DIR_MASK = 0b1111
    # BIT_OUT_MASK = 0b01000100010001000100010001000100
    # BIT_BLACK_MASK = 0b00010001000100010001000100010001
    # BIT_WHITE_MASK = 0b00100010001000100010001000100010

