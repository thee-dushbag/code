from . import hello, shout
import click, time

__all__ = "hello", "shout", "count"
__plugins__ = __all__

COUNT = "Counting from %(start)s to %(stop)s in steps of %(step)s"


class count:
    @click.command
    @click.option("--start", type=int, default=0)
    @click.option("--stop", type=int, default=100)
    @click.option("--step", type=int, default=1)
    @click.option("--sleep", type=click.FloatRange(0, 5, clamp=True), default=0.1)
    @click.option("--message", "-m", default=COUNT)
    @staticmethod
    def __command__(start: int, stop: int, step: int, message: str, sleep: float):
        msg = message % dict(start=start, stop=stop, step=step)
        with click.progressbar(range(start, stop, step), label=msg) as bar:
            for _ in bar:
                time.sleep(sleep)
