from mpack.logging import logger, Level as L
import time, random as rand

class Priority:
    system_high = 5
    system_low = 4
    user_high = 3
    user_low = 2
    low = 1


class Process:
    def __init__(
        self, name: str, shots: int, priority: int = Priority.user_high
    ) -> None:
        self.max_count: int = shots
        self.priority = priority
        self.count = 0
        self.name = name.ljust(10, " ")
        self._total_time = 0

    @property
    def total_time(self) -> str:
        return str(round(self._total_time, 3)).ljust(6, " ")

    @property
    def done(self) -> bool:
        return self.count >= self.max_count

    def run(self, total: int, quanta: float):
        self.count += 1
        self._total_time += quanta
        logger.info(
            "[%s]: time %s: ratio %s"
            % (self.name, self.total_time, round(self.count / total, 2))
        )

    def teardown(self):
        logger.debug(
            "[%s]: priority: %s total: %s seconds"
            % (self.name, self.priority, self.total_time)
        )


class Ticket:
    def __init__(self, tickman: "TickMan") -> None:
        self.manager = tickman


class TickMan:
    def __init__(self, process: Process) -> None:
        self.tickets = [Ticket(self) for _ in range(process.priority)]
        self.owner = process


class Scheduler:
    def __init__(self, quantum: float = 0.5) -> None:
        self.processes: list[Process] = []
        self.managers: list[TickMan] = []
        self.quantum = quantum

    def tickets(self) -> list[Ticket]:
        tickets = []
        for man in self.managers:
            tickets.extend(man.tickets)
        return tickets

    def getnext(self) -> TickMan:
        ticket = rand.choice(self.tickets())
        return ticket.manager

    def process(self):
        runs = 0
        while self.managers:
            runs += 1
            manager = self.getnext()
            manager.owner.run(runs, self.quantum)
            time.sleep(self.quantum)
            if manager.owner.done:
                self.managers.remove(manager) # Remove processor from runnable ones.
                # manager.owner.teardown() # Teardown the process here.
        for process in sorted(self.processes, reverse=True, key=lambda p: p.priority):
            process.teardown()
        logger.warn("Total Processing Time: %s seconds." % (self.quantum * runs))

    def put(self, process: Process):
        self.processes.append(process)
        self.managers.append(TickMan(process))


sched = Process("scheduler", 40, Priority.system_low)
download = Process("ktorrent", 20, Priority.user_low)
file_system = Process("fs", 40, Priority.system_low)
term = Process("terminal", 30, Priority.user_high)
clock = Process("clock", 50, Priority.system_high)
video = Process("vlc", 30, Priority.user_high)
updates = Process("updates", 10, Priority.low)

logger.mute()
logger.turnon(L.DEBUG | L.WARN | L.INFO)
sche = Scheduler(0.005)
sche.put(file_system)
sche.put(download)
sche.put(updates)
sche.put(clock)
sche.put(video)
sche.put(sched)
sche.put(term)
# FIXME: The scheduler is also the CPU, change that.
sche.process()
