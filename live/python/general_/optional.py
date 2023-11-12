from mpack.option import Option, ty
import random

class Employee:
    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self) -> None:
        print(f"Hello {self.name}, how was your day?")
    
    def __str__(self) -> str:
        return f'Employee(name={self.name !r})'


def get_employee() -> ty.Optional[Employee]:
    _names: list[str] = ["Simon", "Nganga", "Njoroge"]
    name = random.choice(_names)
    return None if random.random() < 0.5 else Employee(name)


def chname(name: str):
    def _chname(pe: Employee | None) -> Employee | None:
        if pe is None: return
        return Employee(name)

    return _chname

class ContextLike(ty.Protocol):
    def _enter(self) -> ty.Any: ...
    def _exit(self) -> ty.Any: ...

def Context(obj: ContextLike):
    try:
        val = obj._enter()
        yield val or obj
    finally:
        obj._exit()

class _OpenFile:
    def __init__(self, file: 'File') -> None:
        self.file = file
        self.content = ''
    
    def write(self, text):
        self.content += str(text)
    
    def read(self):
        return self.content

class File:
    def __init__(self, file: str) -> None:
        self.filename = file
    
    def _enter(self) -> _OpenFile:
        print("Opening file:", self.filename)
        return _OpenFile(self)
    
    def _exit(self):
        print("Closing file:", self.filename)

for of in Context(File("hello.txt")):
    print("In scope of:", of.file.filename)
    of.write("Hello World, how are your?")
    # raise FileNotFoundError
    print("File contents:", of.read())

print()

me = Option(get_employee()).value_or(Employee("Faith Njeri"))
print(me)
me.greet()

print()

emp = Option(get_employee())
emp.and_then(lambda e: e.greet())\
    .or_else(lambda: print("Invalid Employee"))\
    .transform(chname("Lydia Njeri"))\
    .and_then(lambda e: e.greet())\
    .or_else(lambda: print("Still Invalid"))
