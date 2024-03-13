from threading import local

_local = local()

def _getos() -> str:
    try:
        os = _local.os
    except AttributeError:
        import sys
        os = sys.platform
        _setos(os)
    return os


def _setos(new: str):
    "Internal API, use setos instead."
    _local.__dict__["os"] = new


def setos(new: str):
    "Set the current os to <new>"
    if not isinstance(new, str):
        raise TypeError("Os name has to be a string")
    _setos(new)


def getos() -> str:
    "Get name of os"
    return _getos()
