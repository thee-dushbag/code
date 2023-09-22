from random import choice

import db
from aiohttp import web
from db import get_app_db
from faker import Faker

fake = Faker()


def setup(app: web.Application, add=True):
    if not add:
        return
