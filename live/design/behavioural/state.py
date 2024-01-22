import typing as ty
from random import randint
from math import log2, ceil


class GuessingGame:
    def __init__(self) -> None:
        self.low: int = 0
        self.high: int = 0
        self.guess: int = 0
        self.score: int = 0
        self.steps: int = 0
        self.tries: int = 0
        self.win: bool = False
        self.state = Loading(self)

    def start(self):
        self.state.start()

    def transition(self, state):
        self.state = state

    def show(self, *things: str):
        for thing in things:
            print(thing)

    def input(self, prompt: str):
        return input(prompt)


class State(ty.Protocol):
    game: GuessingGame

    def start(self):
        ...


class Loading(State):
    def __init__(self, game: GuessingGame) -> None:
        self.game = game

    def load(self):
        self.game.show("Loading Game. (*_*)")

    def start(self):
        self.load()
        state = Menu(self.game)
        self.game.transition(state)
        state.start()


class Saving(State):
    def __init__(self, game: GuessingGame) -> None:
        self.game = game

    def start(self):
        self.game.show("Exiting Game. ByeBye.")


class Playing(State):
    def __init__(self, game: GuessingGame) -> None:
        self.game = game
        self.paused = False

    def guess(self):
        return randint(self.game.low, self.game.high)

    def pause(self):
        pause = Pause(self.game)
        self.game.transition(pause)
        pause.start()
        self.paused = True

    def help(self):
        show = self.game.show
        h, l = self.game.high, self.game.low
        show("Usage: <commands available>")
        show("  help     - Show this help message.")
        show("  pause    - Pause the game.")
        show(f"  <number> - Your guess. Must be in the range {h, l}.")

    def getnumber(self):
        inp = self.game.input("Guess: ")
        if inp == "pause":
            return self.pause()
        if inp == "help":
            return self.help()
        if not inp.isnumeric():
            return self.game.show(
                f"Expected a number, got {inp!r}. Type 'help' for usage help."
            )
        return int(inp)

    def gameover(self):
        over = GameOver(self.game)
        self.game.transition(over)
        over.start()

    def play(self):
        while not self.paused:
            guess = self.getnumber()
            if guess is None:
                continue
            if guess > self.game.guess:
                self.game.show("Too Hot")
            elif guess < self.game.guess:
                self.game.show("Too Cold")
            else:
                self.game.win = True
                return self.gameover()
            if self.game.tries >= self.game.steps:
                return self.gameover()
            self.game.tries += 1

    def setup(self):
        self.game.score = 0
        self.game.guess = self.guess()
        self.game.steps = ceil(log2(self.game.high - self.game.low + 1))

    def start(self):
        if not self.paused:
            self.setup()
        self.game.win = False
        self.paused = False
        self.play()


class Menu(State):
    def __init__(self, game: GuessingGame) -> None:
        self.game = game

    def help(self):
        show = self.game.show
        show("Commands: ")
        show("  high - To set HIGH")
        show("  low  - To set LOW")
        show("  exit  - To exit the game")
        show("  quit  - To exit the game")
        show("  play  - To start the game")

    def play(self):
        self.game.tries = 0
        self.game.guess = 0
        play = Playing(self.game)
        self.game.transition(play)
        play.start()

    def exit(self):
        save = Saving(self.game)
        self.game.transition(save)
        save.start()

    def setup(self):
        h, l = False, False
        while True:
            cmd = self.game.input("> ")
            match cmd:
                case "help":
                    self.help()
                case "high":
                    high = self.game.input("  HIGH=")
                    if not high.isnumeric():
                        self.game.show("Expected an integer for HIGH.")
                    else:
                        h = True
                        self.game.high = int(high)
                case "low":
                    low = self.game.input("  LOW=")
                    if not low.isnumeric():
                        self.game.show("Expected an integer for LOW.")
                    else:
                        l = True
                        self.game.low = int(low)
                case "play":
                    if not h:
                        self.game.show("HIGH was not set.")
                    elif not l:
                        self.game.show("LOW was not set.")
                    else:
                        return self.play()
                case "quit" | "exit":
                    return self.exit()

    def start(self):
        self.game.show("Game Menu")
        self.setup()


class GameOver(State):
    def __init__(self, game: GuessingGame) -> None:
        self.game = game

    def start(self):
        type = (
            f"Won. You found {self.game.guess}."
            if self.game.win
            else f"Lost. Correct guess was {self.game.guess}."
        )
        self.game.show(f"GameOver: You {type}")
        self.game.input("Press <enter> key to continue.")
        menu = Menu(self.game)
        self.game.transition(menu)
        menu.start()


class Pause(State):
    def __init__(self, game: GuessingGame) -> None:
        self.game = game

    def help(self):
        self.game.show("Options:")
        self.game.show("  help")
        self.game.show("  resume")
        self.game.show("  restart")
        self.game.show("  quit/exit")

    def play(self, paused: bool):
        play = Playing(self.game)
        play.paused = paused
        self.game.transition(play)
        play.start()

    def exit(self):
        menu = Menu(self.game)
        self.game.transition(menu)
        menu.start()

    def paused(self):
        while True:
            cmd = self.game.input("Option: ")
            match cmd:
                case "help":
                    return self.help()
                case "resume":
                    return self.play(True)
                case "restart":
                    return self.play(False)
                case "quit" | "exit":
                    return self.exit()
                case _:
                    self.game.show(
                        f"Unknown option {cmd!r}. Enter help for usage help."
                    )

    def start(self):
        self.game.show(f"Game Paused At: tries={self.game.tries}/{self.game.steps}")
        self.help()
        self.paused()


if __name__ == "__main__":
    game = GuessingGame()
    game.start()
