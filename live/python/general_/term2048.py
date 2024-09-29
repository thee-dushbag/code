import pprint as p
import subprocess as sub
from sys import path

import Game2048


def print_matrix(matrix, length, special, __fillch=" ") -> None:
    mutate = []
    orow = []
    for row in matrix:
        mrow = []
        srow = []
        for value in row:
            v = value
            value = " " if value == 0 else value
            svalue = str(value).center(length, __fillch)
            srow.append(svalue)
            if v >= special:
                svalue = "\x1b[92;1m" + svalue + "\x1b[0m"
            elif value != 0:
                svalue = "\x1b[93;1m" + svalue + "\x1b[0m"
            mrow.append(svalue)
        mutate.append("| " + " | ".join(mrow) + " |")
        orow.append("| " + " | ".join(srow) + " |")
    maxlen = max([len(srow) for srow in orow])
    maxlen = "\n+" + ("-" * (maxlen - 2)) + "+" + "\n"
    matrix = maxlen + maxlen.join(mutate) + maxlen
    print(matrix)


help_txt = """2048 Help Text.
Actions:
    w -> up
    a -> left
    s -> down
    d -> right
    q -> quit
    h -> help

Format: (<digit>*<action>)+
Example: 20w5sd
         Means make 20 up, 5 down and 1 left.
"""

def expand_input(input_str: str) -> list[str]:
    chars, action = [], []
    for char in input_str:
        if char.isdigit():
            chars.append(char)
        else:
            count = int("".join(chars)) if chars else 1
            action.extend(char * count)
            chars.clear()
    return action

def main() -> None:
    game = Game2048.Game2048()
    dim = 8
    game.new_game(dim=dim, hscore=2048)
    one = True
    cell = 4
    game_title = (
        "\x1b[4;94;1m" + "2048 Game.".center(cell * dim + 4 * dim, " ") + "\x1b[0m"
    )
    while True:
        if game.check_game_over():
            sub.run("clear", shell=True)
            print(game_title)
            print_matrix(game.matrix, cell, game.hscore)
            print(f"\x1b[97;1mHighest : \x1b[92;1m{game.highest}\x1b[0m")
            print(f"\x1b[97;1mTarget  : \x1b[92;1m{game.hscore}\x1b[0m")
            if game.hscore_reached:
                print(
                    f"\x1b[91;1mGameOver: \x1b[92;1mYou Win \x1b[96;1m(*_*)\x1b[93;1m\nScore: \x1b[92;1m{game.score}\x1b[0m\n"
                )
            else:
                print(
                    f"\x1b[91;1mGameOver: \x1b[96;1mYou Lose \x1b[97;1m(O_O)\x1b[93;1m\nScore: \x1b[92;1m{game.score}\x1b[0m\n"
                )
            break
        sub.run("clear", shell=True)
        print(game_title)
        game.set_highest()
        print(f"\x1b[97;1m\nScore   : \x1b[92;1m{game.score}\x1b[0m")
        print(f"\x1b[97;1mHighest : \x1b[92;1m{game.highest}\x1b[0m")
        print(f"\x1b[97;1mTarget  : \x1b[92;1m{game.hscore}\x1b[0m")
        print_matrix(game.matrix, cell, game.hscore)
        if one:
            print(help_txt)
            one = False
        print("Enter action: w, s, a, d, q, h")
        actions = input("action:> ")
        for action in expand_input(actions):
            if action == "w":
                game.slide_up()
            elif action == "s":
                game.slide_down()
            elif action == "a":
                game.slide_left()
            elif action == "h":
                one = True
            elif action == "d":
                game.slide_right()
            elif action == "q":
                print("\x1b[91;1mQuitting the game.\x1b[0m")
                exit(0)
            else:
                one = True


if __name__ == "__main__":
    main()
