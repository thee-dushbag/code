import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from faker import Faker

DB_STORE_KEY = "user_database_data_store"
CHECK_AUTH_KEY = "user_database_check_auth"

fake = Faker()
fake.age = lambda: fake.random_int(5, 65)  # type: ignore[attr]


@dataclass
class User:
    name: str = field(default_factory=fake.name)
    age: int = field(default_factory=fake.age)
    email: str = field(default_factory=fake.email)
    password: str = field(default_factory=fake.password)

    def to_dict(self):
        return asdict(self)


class UserData:
    def __init__(self, username: str, password: str) -> None:
        self.data = {}
        self.username = username
        self.password = password

    def __eq__(self, other: "UserData"):
        if type(other) != UserData:
            other = UserData(str(other), "")
        return self.username == other.username

    def __hash__(self) -> int:
        return hash(self.username)

    def authenticate(self, name: str, passwd: str):
        return name == self.username and passwd == self.password

    def to_dict(self):
        return dict(username=self.username, password=self.password, userdata=self.data)

    @staticmethod
    def create_userdata(username, password, userdata=None):
        user = UserData(username, password)
        user.data = userdata or {}
        return user


class DatabaseStore:
    def __init__(self, store_file: str, key=None) -> None:
        self.users: list[UserData] = []
        self.store = Path(store_file)
        self.key = key or "users"

    def load_users(self):
        users = []
        if self.store.exists():
            ustr = self.store.read_text()
            users = json.loads(ustr).pop(self.key)
        for user in users:
            userdata = UserData.create_userdata(**user)
            self.users.append(userdata)

    def save_users(self):
        if self.store.exists():
            self.store.unlink()
            self.store.touch()
        jdict = {self.key: [user.to_dict() for user in self.users]}
        ustr = json.dumps(jdict)
        self.store.write_text(ustr)

    def add_user(self, user: UserData):
        if user not in self.users:
            self.users.append(user)
            return True

    def rm_user(self, username: str, password: str):
        if tuser := self.get_user(username, password):
            self.users = [user for user in self.users if user != tuser]
            return True

    def get_user(self, name, password):
        for user in self.users:
            if user.authenticate(name, password):
                return user

    def auth_user(self, username, password):
        return self.get_user(username, password)
