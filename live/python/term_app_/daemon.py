import asyncio as aio
from term import Term, TermArgsError
from typing import cast

class Counter:
    def __init__(self, start, stop, step, delay=.5) -> None:
        self.current: float = start
        self.stop: float = stop
        self.step: float = step
        self.delay: float = delay
        self.is_counting = False
    
    async def count(self):
        self.is_counting = True
        while self.current < self.stop:
            await aio.sleep(self.delay)
            self.current += self.step
        self.is_counting = False

def set_counter_current(term: Term, cmd: str, args: tuple[str, ...], kwargs: dict):
    if not args:
        raise TermArgsError
    try:
        start = int(args[0])
    except Exception:
        raise TermArgsError
    counter: Counter | None = term.namespace.get('counter')
    if counter and counter.is_counting:
        counter = cast(Counter, counter)
        counter.current = start
        print(f"Set Counter Current: {start}")

def set_counter_step(term: Term, cmd: str, args: tuple[str, ...], kwargs: dict):
    if not args:
        raise TermArgsError
    try:
        start = float(args[0])
    except Exception:
        raise TermArgsError
    counter: Counter | None = term.namespace.get('counter')
    if counter and counter.is_counting:
        counter = cast(Counter, counter)
        counter.step = start
        print(f"Set Counter Step: {start}")


def get_current_counter(term: Term, *_):
    counter: Counter | None = term.namespace.get('counter')
    counter = cast(Counter, counter)
    print(f"Counter current: {counter.current}")

def get_current_step(term: Term, *_):
    counter: Counter | None = term.namespace.get('counter')
    counter = cast(Counter, counter)
    print(f"Counter step: {counter.step}")