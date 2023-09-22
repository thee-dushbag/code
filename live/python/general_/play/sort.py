from functools import partial
from pathlib import Path

BASE_NAME = "Bless.This.Mess.Sn2.Ep{ep}{suff}"
cname = lambda ep, suff: BASE_NAME.format(ep=ep, suff=suff)
ename = partial(cname, suff=".mp4")

4771

shows = [
    ("", 1),
    ("", 2),
    ("", 3),
    ("", 4),
    ("", 5),
    ("", 6),
    ("", 7),
    ("", 8),
    ("", 9),
    ("", 10),
    ("", 11),
    ("", 12),
    ("", 13),
    ("", 14),
    ("", 15),
    ("", 16),
    ("", 17),
    ("", 18),
    ("", 19),
    ("", 20),
    # ('', 21),
    # ('', 22),
    # ('', 23),
]

TargetDir = Path.home() / "Desktop" / "toSort"

for path in TargetDir.iterdir():
    for name, ep in shows:
        if path.name.startswith(name):
            path.rename(path.parent / ename(ep))
