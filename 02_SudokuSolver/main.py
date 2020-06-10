class Sudoku:
    def __init__(self, L, initial):
        self.L = L
        self.solution = initial
        self.bind_area = []
        for h in range(self.L**2):
            tmp_h = []
            tmp_w = []
            for w in range(self.L**2):
                tmp_h.append((h, w))
                tmp_w.append((w, h))
            self.bind_area.append(tmp_h)
            self.bind_area.append(tmp_w)

        self.bind_square = []
        for lh in range(0, self.L**2, self.L):
            for lw in range(0, self.L**2, self.L):
                tmp = []
                for dh in range(self.L):
                    for dw in range(self.L):
                        nh, nw = lh + dh, lw + dw
                        tmp.append((nh, nw))
                self.bind_square.append(tmp)
        self.bind_area += self.bind_square
        # print(*self.bind_area, sep="\n")
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
            h = i // (self.L**2)
            w = i % (self.L**2)
            if solution[h][w] == -1:
                continue

            s = solution[h][w]

            for th, tw in self.getRelativeArea(h, w):
                possibility[th][tw][s] = False
        return

    def selectOneChoice(self, possibility, solution, bind):
        # poss = possibilities
        flag = False

        for i in range(1, self.L**2 + 1):
            tmp = []
            for h, w in bind:
                if possibility[h][w][i] is True:
                    tmp.append((h, w))
            if len(tmp) != 1:
                continue
            h, w = tmp[0]
            if solution[h][w] == i:
                continue

            flag = True
            h, w = tmp[0]
            possibility[h][w] = {j: False for j in range(1, self.L**2 + 1)}
            possibility[h][w][i] = True
            solution[h][w] = i

        return flag

    def isValidSolution(self, solution):
        for area in self.bind_area:
            tmp = {i: False for i in range(1, self.L**2 + 1)}
            for h, w in area:
                if solution[h][w] == -1:
                    continue

                if tmp[solution[h][w]] is True:
                    print("Conflict!", h, w)
                    return False
                else:
                    tmp[solution[h][w]] = True
        return True

    def deletePossibility(self, possibility, solution, bind):
        flag = False
        for i in range(1, self.L**2 + 1):
            if any(solution[h][w] == i for h, w in bind) is True:
                continue
            tmp_h = set()
            tmp_w = set()
            for h, w in bind:
                if possibility[h][w][i] is True:
                    tmp_h.add(h)
                    tmp_w.add(w)

            if len(tmp_h) == 1:
                h = list(tmp_h)[0]
                for w in range(self.L**2):
                    if (h, w) not in bind and possibility[h][w][i] is True:
                        flag = True
                        possibility[h][w][i] = False
            if len(tmp_w) == 1:
                w = list(tmp_w)[0]
                for h in range(self.L**2):
                    if (h, w) not in bind and possibility[h][w][i] is True:
                        flag = True
                        possibility[h][w][i] = False
        return flag

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
                print("Define Solution", True)
                flag = True
                solution[h][w] = keys[0]

        for bind in self.bind_area:
            tmp = self.selectOneChoice(possibility, solution, bind)
            flag = flag or tmp
            # print("selectOne", tmp)

        for bind in self.bind_square:
            tmp = self.deletePossibility(possibility, solution, bind)
            flag = flag or tmp
            # print(tmp, bind)
            # print("delete", tmp)

        return flag and self.isValidSolution(solution)

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
        i = 0
        while flag is True:
            print("update!", i)
            flag = self.updateSolution(solution, possibility)
            if self.isSolved(solution) is True:
                break
            i += 1

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
