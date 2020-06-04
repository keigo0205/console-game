class Sudoku:
    def __init__(self, L, initial):
        self.L = L
        self.solution = initial
        return

    def __str__(self):
        ret = ''
        for line in self.solution:
            ret += " ".join(line) + "\n"
        return ret

    def getRelativeArea(self, H, W):
        for h in range(self.L**2):
            if h != H:
                yield h, W
        for w in range(self.L**2):
            if w != W:
                yield H, w

        lh, lw = (H // self.L) * self.L, (W // self.L) * self.L
        for dh in range(self.L):
            for dw in range(self.L):
                nh, nw = lh + dh, lw + dw
                if nh != H or nw != W:
                    yield nh, nw

    def updatePossiblity(self, solution, possibility):
        for i in range((self.L**2)**2):
            h = i // self.L**2
            w = i % self.L**2
            if solution[h][w] == -1:
                continue

            s = solution[h][w]

            for th, tw in self.getRelativeArea(h, w):
                possibility[th][tw][s] = False
        return

    def updateSolution(self, solution, possibility):
        flag = False
        self.updatePossiblity(solution, possibility)

        for i in range((self.L**2)**2):
            h = i // self.L**2
            w = i % self.L**2
            if solution[h][w] != -1:
                continue
            keys = [k for k, v in possibility[h][w].items() if v is True]
            if len(keys) == 1:
                flag = True
                solution[h][w] = keys[0]

        return flag

    def isSolved(self, solution):
        for i in range(self.L**2**2):
            h, w = i // self.L**2, i % self.L**2
            if solution[h][w] == -1:
                return False
        return True

    def solve(self):
        solution = [[-1] * self.L**2 for _ in range(self.L**2)]
        possibility = [[{i + 1: True for i in range(self.L**2)} for _ in range(self.L**2)] for _ in range(self.L**2)]

        for i in range((self.L**2)**2):
            h = i // self.L**2
            w = i % self.L**2
            s = self.solution[h][w]
            if s.isdigit() is True:
                solution[h][w] = int(s)
                possibility[h][w] = {i + 1: False for i in range(self.L**2)}
                possibility[h][w][int(s)] = True

        flag = True
        while flag is True:
            flag = self.updateSolution(solution, possibility)
            if self.isSolved(solution) is True:
                break

        for i in range(self.L**4):
            h, w = i // self.L**2, i % self.L**2
            if solution[h][w] != -1:
                self.solution[h][w] = str(solution[h][w])

        return


def main():
    print("import suudoku problem")
    L = int(input())
    initial = [input().split() for _ in range(L**2)]
    game = Sudoku(L, initial)

    # print(game)
    print()
    print("solving ...")
    print()
    game.solve()
    print(game)

    return


if __name__ == '__main__':
    main()
