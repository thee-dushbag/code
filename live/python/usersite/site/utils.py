import json
from random import choice

from aiohttp import web as _web
from exc import State
from faker import Faker
from usite import USERSITE
from usite import UserSite as _UserSite


def signup_random_users(usersite: _UserSite, fake: Faker, n: int, addme: bool = True):
    users = []
    _users = get_sample_users(n, fake)
    if addme:
        _users.append(me)
    for user in _users:
        status = usersite.signup(**user)
        user["status"] = status.to_dict()
        users.append(user)
    with open("states.json", "w") as s:
        json.dump(dict(users=users), s)


def get_sample_users(n: int, fake: Faker) -> list[dict]:
    _p = lambda: choice(["gmail", "hotmail", "thunderbird", "outlook", "yahoo"])
    _e = lambda p: f'@{p}.{choice(["com", "mil", "xyz"])}'
    gen_email = lambda name: name.replace("_", "").lower() + _e(_p())

    def gen_user(fake: Faker):
        name = fake.name().replace(" ", "_")
        pword = fake.password(25, 0, 0, 0)
        email = gen_email(name)
        return dict(name=name, password=pword, email=email)

    return [gen_user(fake) for _ in range(n)]


def get_login_data() -> tuple[str, str]:
    name = input("Name    : ")
    password = input("Password: ")
    return name, password


me = dict(name="Simon", password="1234", email="simongash@gmail.com")


def get_user_site(req: _web.Request, app_key=None) -> _UserSite:
    return req.app[app_key or USERSITE]


def logged_in(req: _web.Request, uid: int) -> bool | None:
    site = get_user_site(req)
    user = site.manager.get_user(uid)
    if user.state == State.SUCCESS:
        if user.result.name in site.logged_in:
            return True
