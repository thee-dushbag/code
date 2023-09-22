import asyncio as aio
from typing import Sequence

from daemon import (Counter, get_current_counter, get_current_step,
                    set_counter_current, set_counter_step)
from term import Term


async def main(argv: Sequence[str]) -> None:
    term = Term("> ")
    term.commands["set_current"] = set_counter_current
    term.commands["get_current"] = get_current_counter
    term.commands["get_step"] = get_current_step
    term.commands["set_step"] = set_counter_step
    counter = Counter(1, 1000, 1, 1)
    term.namespace["counter"] = counter
    try:
        await aio.gather(counter.count(), term.run_forever(), return_exceptions=True)
    except aio.CancelledError:
        pass


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
