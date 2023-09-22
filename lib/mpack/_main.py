__all__ = "main", "get_modname"


def main(mod=None, *, target: str = "__main__"):
    def _get_main(func=None, /, **kwargs):
        def _caller(main_func):
            nonlocal mod
            if callable(mod):
                mod = None
            if mod is None or mod == target:
                main_func(**kwargs)
            main_func.__main_kwargs__ = kwargs
            return main_func

        return _caller(func) if func else _caller

    return _get_main(mod) if callable(mod) else _get_main


def get_modname(file: str):
    from pathlib import Path

    return Path(file).stem
