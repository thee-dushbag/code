"""
This is a package containing all my python reusable code projects.
My greatest being the number_reader.
Import from _init for the init values, moved due to dependencies.
"""

def __getattr__(name: str):
    if name == 'main':
        from ._init import main
        return main
    raise AttributeError(name)

