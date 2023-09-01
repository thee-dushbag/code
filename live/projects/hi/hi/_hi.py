from typing import Optional

__all__ = 'hi', 'say_hi'

HI_FORMAT = 'Hello {name}, how was your day?'
NAME_KEY = 'name'

def hi(name: str, *, format: str=HI_FORMAT, key: str = NAME_KEY) -> str:
    f'''Say hi to a given name using a given Hi_FORMAT
    default: HI_FORMAT '{HI_FORMAT}'
        >>> hi('Simon')
        Hello Simon, how was your day?
        >>> hi('Mark', 'Hi %(name)s?')
        Hi Mark
    '''
    data = {key: name}
    return format.format(**data)

def say_hi(name: str, *, format: Optional[str] = None, key: Optional[str] = None):
    f'print(hi(name, format=format or HI_FORMAT))'
    print(hi(name, format=format or HI_FORMAT, key = key or NAME_KEY))