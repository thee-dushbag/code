import asyncio as aio
from typing import Sequence
from signal import strsignal, signal

async def main(argv: Sequence[str]) -> None:
    ...

def sig_handler(sig: int,  *_):
    strsig = strsignal(sig) or f"<UNKNOWN_SIG({sig})>"
    print(f"Received SIGNAL: {strsig}")

for i in range(1, 100):
    try:
        signal(i, sig_handler)
    except:
        pass

if __name__ == '__main__':
    from sys import argv
    while True: pass
