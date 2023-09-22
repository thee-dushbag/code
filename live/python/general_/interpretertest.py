# type: ignore
import signal
import sys as _s

_s.path.append("/home/simon/Content/code/projects")
from math_interpreter import parser


def cmd_math() -> None:
    signal.signal(2, lambda *_: exit(0))
    print("Enter 'exit' or 'x' or ctrl+c to exit interpreter.")
    while True:
        try:
            pmt = input("exp:> ")
            if pmt in ["exit", "x"]:
                return
            sol = parser.parse(pmt)
            print(f"{pmt} = {sol}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    cmd_math()
