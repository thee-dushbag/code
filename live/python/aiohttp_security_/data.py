import db
from faker import Faker
from random import choice
from aiohttp import web
from db import get_app_db

fake = Faker()

def setup(app: web.Application, add=True):
    if not add: return