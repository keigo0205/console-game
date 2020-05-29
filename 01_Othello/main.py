from subprocess import call
from copy import copy
from getch import getch
from random import choice


class othello:
    def __init__(self):
        self.height = 8
        self.width = 8
        self.empty = "·"
        self.board = [[self.empty for _ in range(
            self.width)] for _ in range(self.height)]
        self.black = "●"
        self.white = "○"
        self.turn = self.black
        self.opponent = self.white
        self.py = 0
        self.px = 0
        self.player = {self.black: None, self.white: None}
        return

    def __str__(self, key=True):
        call("clear")
        ret = ""
        for i in range(self.height):
            tmp = copy(self.board[i])
            if self.py == i and (key is True):
                tmp[self.px] = "*"
            ret += " ".join(tmp) + "\n"
        ret += "turn: " + self.turn + "\n"
        ret += "how to play\n"
        ret += "a : ←, "
        ret += "w : ↑, "
        ret += "d : →, "
        ret += "s : ↓, "
        ret += "Enter : put\n"
        ret += "Q : quit game"
        return ret

    def print_menu(self, mode_f, mode_s, key):
        call("clear")
        print("Othello Game")
        print("please select mode")
        for k, f, s in zip(key, mode_f, mode_s):
            print(" ".join([k, f, "vs", s]))
        print("w: ↑, s: ↓, enter: select")
        return

    def select_mode(self):
        call("clear")
        mode_f = ["human", "human", "cpu"]
        mode_s = ["human", "cpu", "cpu"]
        k = 0
        key = [" " for i in range(len(mode_f))]
        key[k] = "→"
        self.print_menu(mode_f, mode_s, key)
        while True:
            get = getch()
            if get == "w":
                k = max(0, k - 1)
            elif get == "s":
                k = min(len(mode_f) - 1, k + 1)
            elif get == "\n":
                break
            key = [" " for i in range(len(mode_f))]
            key[k] = "→"
            self.print_menu(mode_f, mode_s, key)
        return mode_f[k], mode_s[k]

    def start(self):
        self.board[3][3] = self.white
        self.board[4][4] = self.white
        self.board[3][4] = self.black
        self.board[4][3] = self.black
        print(self)
        return

    def change_turn(self):
        self.turn = [self.black, self.white][self.turn == self.black]
        self.opponent = [self.black, self.white][self.turn == self.black]

    def canPut_line(self, h, w, x, y):
        h += y
        w += x
        if (0 <= h < self.height and 0 <= w < self.width) is False:
            return False
        elif self.board[h][w] != self.opponent:
            return False

        h += y
        w += x
        while 0 <= h < self.height and 0 <= w < self.width:
            # print(h, w)
            if self.board[h][w] == self.turn:
                return True
            h += y
            w += x
        return False

    def canPut(self, h, w):
        if self.board[h][w] != self.empty:
            return False
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                if self.canPut_line(h, w, x, y) is True:
                    return True
        return False

    def check(self):
        for i in range(self.height * self.width):
            if self.board[i // self.width][i % self.width] != self.empty:
                continue
            elif self.canPut(i // self.width, i % self.width) is True:
                return True
        return False

    def changeColor(self, py, px):
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                elif self.canPut_line(py, px, x, y) is False:
                    continue
                ty = py + y
                tx = px + x
                while self.board[ty][tx] != self.turn:
                    self.board[ty][tx] = self.turn
                    ty += y
                    tx += x
        return

    def count(self, color):
        return sum(A.count(color) for A in self.board)

    def humanSelect(self):
        print(self)
        while True:
            get = getch()
            if get == "a":
                self.px = max(0, self.px - 1)
            elif get == "d":
                self.px = min(self.width - 1, self.px + 1)
            elif get == "w":
                self.py = max(0, self.py - 1)
            elif get == "s":
                self.py = min(self.height - 1, self.py + 1)
            elif get == "Q":
                print("Quit")
                exit()
            elif get == "\n":
                if self.canPut(self.py, self.px) is False:
                    print("You cannot put here.")
                    continue
                break
            print(self)

        return

    def cpuSelect(self):
        canP = self.canPut
        he = self.height
        wi = self.width
        flag = [i for i in range(he * wi) if canP(i // he, i % wi) is True]
        tmp = choice(flag)
        self.py = tmp // he
        self.px = tmp % wi
        return
