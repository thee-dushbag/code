from typing import Callable, Sequence, Any

class API_Context:
    def __init__(self, *data: str | int) -> None:
        self.data = list(data)
    def add(self, *data: str | int):
        self.data.extend(data)
    def __str__(self) -> str:
        return f'API({self.data})'
    def get(self):
        if self.data:
            return self.data.pop()
        return
    
    def source(self, func: Callable):
        self.add(self._source(func)())
    
    def _source(self, func: Callable):
        def wrap(*a: Any, **k: Any):
            return func(*a, **k)
        return wrap

    def source_call(self, func: Callable):
        def wrap(*a: Any, **k: Any):
                val = self._source(func)(*a, **k)
                self.add(val)
        return wrap

context = API_Context()

@context.source_call
def get_api_one(num: int): return num * 'one'
@context.source_call
def get_api_two(num: int): return num * 'two'
@context.source_call
def get_api_thr(num: int): return num * 'three'
@context.source_call
def get_api_for(num: int): return num * 'four'
@context.source_call
def get_api_fiv(num: int): return num * 'five'


def main(argv: Sequence[str]) -> None:
    # print(context)
    # for func in (get_api_one, get_api_two, get_api_thr, get_api_for, get_api_fiv):
    #     context.add(func())
    get_api_fiv(2)
    get_api_for(10)
    print(context)

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])