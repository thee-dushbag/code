from mypyutils import events as ev
import threading as th
import time as tm
from typing import Any, Callable, Literal

class Processor:
    def __init__(self, result: Any, ptime: float) -> None:
        self.result= result
        self.ptime:float = ptime + tm.time()

    def done(self) -> bool:
        return tm.time() >= self.ptime

    def __call__(self) -> None:
        print("Processing started.")
        while not self.done():
            print(f"Processing... {int(self.ptime - tm.time() + 1)}")
            tm.sleep(1)
        print("Processing done.")

    def get_result(self) -> Any | Literal[':ResultNotReady:']:
        return self.result if self.done() else ":ResultNotReady:"

class MyProcessor(Processor):
    def __init__(self, callback: Callable[..., Any], result: Any, ptime: float) -> None:
        print(f"Shiro Sent: {result}")
        super().__init__(result, ptime)
        self.callback = callback
    
    def __call__(self) -> None:
        super().__call__()
        self.callback()

def wait_for_res(name: str, processor: Processor) -> None:
    print(f"{name} Received: {processor.get_result()}")

class CallbackFunctor:
    def __init__(self, event: ev.Event, eventmsg: str) -> None:
        self.event: ev.Event = event
        self.eventmsg: str = eventmsg

    def __call__(self) -> Any:
        self.event.emit(self.eventmsg)

def main() -> None:
    event: ev.Event = ev.Event()
    eventmsg: Literal['processor-done'] = 'processor-done'
    callback: CallbackFunctor = CallbackFunctor(event, eventmsg)
    processor: MyProcessor = MyProcessor(callback, "Tukutane SPA003 for IAP class.", 5)
    thread: th.Thread = th.Thread(target=processor)
    thread.start()
    for name in ['Simon', 'Nganga', 'Njoroge', 'Faith', 'Njeri']:
        event.listen(eventmsg, wait_for_res, name, processor)
    thread.join()

if __name__ == '__main__':
    main()