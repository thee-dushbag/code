'''
Manage int bit masks using well defined functions
which improve readability and reduce redunduncy.
1. turnon -> sets specified bits to 1
2. turnoff -> sets specified bits to 0
3. ison -> checks if all specified bits are 1
4. isoff -> checks if all specified bits are 0
'''

__all__ = 'turnon', 'turnoff', 'ison', 'isoff'

def turnon(mask: int, flag: int, /) -> int:
    'sets all bits in either flag or mask to on'
    return mask | flag


def turnoff(mask: int, flag: int, /) -> int:
    'sets all common on bits in flag and mask to off'
    return mask ^ (mask & flag)


def ison(mask: int, flag: int, /) -> bool:
    'checks is all bits(flag) are on in bits(mask)'
    return mask & flag == flag


def isoff(mask: int, flag: int, /) -> bool:
    'checks is all bits(flag) are off in bits(mask)'
    return mask & flag == 0
