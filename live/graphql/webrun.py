from uvloop import install as install_uvloop
from main import application
from aiohttp import web
from os import getenv
from sys import argv

PORT = 5052
STATICS_HOST = getenv("STATICS_HOST")

if len(argv) >= 2 and argv[1].isnumeric():
    PORT = int(argv[1])

try:
    install_uvloop()
    web.run_app(application(), host=STATICS_HOST, port=PORT)
except KeyboardInterrupt:
    ...
