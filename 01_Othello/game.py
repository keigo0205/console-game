import main
import time


game = main.othello()
first, second = game.select_mode()
game.player[game.black] = first
game.player[game.white] = second
game.start()
t = 0
while True:
    B = game.count(game.black)
    W = game.count(game.white)
    if B == 0 or W == 0:
        break
    elif B + W == game.width * game.height:
        break
    if game.check() is False:
        print("You cannot put!!")
        print("Change turn in 2 seconds")
        time.sleep(2)
        game.change_turn()
        print(game)
        continue

    if game.player[game.turn] == "human":
        game.humanSelect()
    elif game.player[game.turn] == "cpu":
        game.cpuSelect()

    game.board[game.py][game.px] = game.turn
    game.changeColor(game.py, game.px)
    game.change_turn()
    print(game)

print(game.__str__(key=False))
B = game.count(game.black)
W = game.count(game.white)
print("Black", B, "-", W, "White")
if B == W:
    print("Draw!!")
elif B > W:
    print("Black Win!!")
elif W > B:
    print("White Win!!")
