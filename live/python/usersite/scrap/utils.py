import json
from pathlib import Path
from random import choice
from bs4 import BeautifulSoup
from faker import Faker
from perfectdict import perfect_dict
from usersiteclient import User


async def create_user(fake: Faker) -> User:
    async def _create_email_for(name: str) -> str:
        name = name.replace("_", "").lower()
        return await random_email_domain(name)

    name: str = fake.name().replace(" ", "_")
    password: str = str(fake.random_int(10**4, 10**6))
    email: str = await _create_email_for(name)
    return User(name=name, password=password, email=email)


async def random_email_domain(username: str):
    email_domain_names: tuple[str, ...] = (
        "gmail",
        "outlook",
        "yahoo",
        "hotmail",
        "thunderbird",
    )
    dot_coms: tuple[str, ...] = ("com", "mil", "xyz", "abc")
    return f"{username}@{choice(email_domain_names)}.{choice(dot_coms)}"


def save_all(filepath: str, data: dict, *, overwrite: bool = False):
    path = Path(filepath)
    if path.exists():
        assert path.is_file(), f"Path({filepath !r}) is not a file path"
    pdata: perfect_dict = perfect_dict(**data)
    content = {}
    if overwrite:
        path.unlink(True)
    if path.exists():
        content: dict[str, dict[str, str]] = json.loads(path.read_text())
    pdata.perfect_update(content)
    with open(filepath, "w") as f:
        json.dump(pdata, f)


async def get_welcome(content: str, parser: str | None = None):
    soup = BeautifulSoup(content, parser or 'lxml')
    welcome = soup.find('h2', attrs={'id': 'welcome'})
    return welcome.text if welcome else 'Not Welcomed'


def load_users(filename: str, key: str | None = None) -> list[dict]:
    path = Path(filename)
    if path.exists() and path.is_file():
        return json.loads(path.read_text())[key or 'users']
    return []