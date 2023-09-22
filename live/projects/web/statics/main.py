import subprocess as _subp
from pathlib import Path
from sys import argv, exit

from aiohttp import web
from aiohttp_cors import setup

STATIC_PATH = Path(Path.cwd() / "static")

if not STATIC_PATH.exists():
    STATIC_PATH.mkdir()


app = web.Application()
cors = setup(app)
app.add_routes([web.static("/", STATIC_PATH)])

if __name__ == "__main__":
    appstring = argv[0].rpartition(".")[0] + ":app"
    try:
        exit(
            _subp.run(
                f"gunicorn -k aiohttp.worker.GunicornWebWorker -b localhost:4567 --reload {appstring}",
                shell=True,
            ).returncode
        )
    except KeyboardInterrupt:
        print("Killing Workers")
