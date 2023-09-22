import json
from cProfile import label
from enum import Enum
from random import choice
from typing import Any, Type, cast

import bcrypt
import sqlalchemy as sa
from faker import Faker
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import declarative_base, sessionmaker

metadata = sa.MetaData()
Base: Type = declarative_base(metadata=metadata)
engine = sa.create_engine("sqlite:///users.db")
Session = sessionmaker(engine)
FORMAT = "utf-8"


class User(Base):
    __tablename__ = "users"
    uid = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), index=True, nullable=False, unique=True)
    email = sa.Column(sa.String(50), index=True, nullable=False, unique=True)
    password = sa.Column(sa.String(50), nullable=False)

    def __str__(self):
        return f"User(name={self.name!r}, password={self.password!r}, email={self.email!r})"


metadata.create_all(engine)

session: _Session = Session()


class mAuto:
    def __set_name__(self, _, name: str):
        self.name = name

    def __get__(self, *_):
        return self.name


class OpType(Enum):
    CHECK_AUTH = mAuto()
    ADD_USER = mAuto()
    UPDATE_USER = mAuto()
    DELETE_USER = mAuto()
    GET_USER = mAuto()
    GET_USERID = mAuto()


class State(Enum):
    SUCCESS = mAuto()
    FAILURE = mAuto()


class OperationStatus:
    def __init__(self, optype: str, state: str, message: str, *, result: Any = None):
        self.optype = optype
        self.message = message
        self.state = state
        self.result = result

    def to_dict(self):
        return dict(
            message=self.message,
            operation_type=self.optype,
            state=self.state,
            string=str(self),
        )

    def __str__(self):
        return f"[{self.optype}][{self.state}]: {self.message}"


class UserManager:
    def __init__(self, session: _Session) -> None:
        self.session: _Session = session

    def add_user(self, name: str, password: str, email: str):
        user = User(name=name, password=password, email=email)
        self.session.add(user)
        optype = OpType.ADD_USER
        try:
            self.session.commit()
        except IntegrityError as e:
            state = State.FAILURE
            message = str(e)
        else:
            state = State.SUCCESS
            message = f"Added User {name}"
        return OperationStatus(optype, state, message)

    def update_user(
        self,
        uid: int,
        *,
        name: str | None = None,
        password: str | None = None,
        email: str | None = None,
    ):
        optype = OpType.UPDATE_USER
        try:
            user = self.session.query(User).where(User.uid == uid).one()
            for key, val in (("name", name), ("email", email), ("password", password)):
                if val:
                    setattr(user, key, val)
            self.session.add(user)
            self.session.commit()
        except (MultipleResultsFound, NoResultFound, IntegrityError) as e:
            state = State.FAILURE
            message = str(e)
        else:
            state = State.SUCCESS
            message = "Updated User Ok"
        return OperationStatus(optype, state, message)

    def get_user(self, uid: int, *, remove: bool = False):
        optype = OpType.DELETE_USER if remove else OpType.GET_USER
        user = None
        try:
            user = self.session.query(User).where(User.uid == uid).one()
            if remove:
                self.session.delete(user)
        except (MultipleResultsFound, NoResultFound) as e:
            state = State.FAILURE
            message = str(e)
        else:
            state = State.SUCCESS
            message = "Found User"
            if remove:
                message += " and Deleted"
        return OperationStatus(optype, state, message, result=user)

    def get_userid(self, name: str):
        optype = OpType.GET_USERID
        userid = None
        try:
            userid = self.session.query(User).where(User.name == name).one().uid
        except (MultipleResultsFound, NoResultFound) as e:
            state = State.FAILURE
            message = str(e)
        else:
            state = State.SUCCESS
            message = "Found UserID"
        return OperationStatus(optype, state, message, result=userid)


class UserSite:
    def __init__(self, manager: UserManager) -> None:
        self.logged_in: dict[str, User] = {}
        self.manager = manager

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        bpass = password.encode(FORMAT)
        epass = bcrypt.hashpw(bpass, salt)
        return epass.decode(FORMAT)

    def _check_password(self, userpw: str, hashedpw: str) -> bool:
        upass = userpw.encode(FORMAT)
        hpass = hashedpw.encode(FORMAT)
        return bcrypt.checkpw(upass, hpass)

    def login(self, *, name: str, password: str):
        optype = OpType.CHECK_AUTH
        uid_: OperationStatus = self.manager.get_userid(name)
        if uid_.state != State.SUCCESS:
            return OperationStatus(optype, State.FAILURE, "Record Not Found")
        user = self.manager.get_user(cast(int, uid_.result))
        hashed_pw = cast(str, user.result.password)
        if self._check_password(password, hashed_pw):
            self.logged_in[cast(str, user.result.name)] = cast(User, user)
            return OperationStatus(optype, State.SUCCESS, "Login Ok")
        return OperationStatus(optype, State.FAILURE, "Login Error")

    def signup(self, *, name: str, password: str, email: str):
        hashedpw = self._hash_password(password)
        status = self.manager.add_user(name, hashedpw, email)
        if status.state != State.SUCCESS:
            return OperationStatus(status.optype, State.FAILURE, "Signup Error")
        return OperationStatus(status.optype, status.state, "Signup Ok")

    def logout(self, name: str):
        if name in self.logged_in:
            self.logged_in.pop(name)

    def change_password(self, name: str, password: str, new_password: str):
        optype = OpType.CHECK_AUTH
        uid_: OperationStatus = self.manager.get_userid(name)
        if uid_.state != State.SUCCESS:
            return OperationStatus(optype, State.FAILURE, "Record Not Found")
        user = self.manager.get_user(cast(int, uid_.result))
        hashedpw = cast(str, user.result.password)
        if self._check_password(password, hashedpw):
            new_hashedpw = self._hash_password(new_password)
            self.manager.update_user(uid_.result, password=new_hashedpw)
            return OperationStatus(optype, State.SUCCESS, "Change Password Ok")
        return OperationStatus(optype, State.FAILURE, "Change Password Error")


from typing import Sequence


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


def main(argv: Sequence[str]) -> None:
    fake = Faker()
    manager = UserManager(session)
    usersite = UserSite(manager)
    name, pword = get_login_data()
    status = usersite.login(name=name, password=pword)
    print(status)
    # signup_random_users(usersite, fake, 5)


def signup_random_users(usersite: UserSite, fake: Faker, n: int, addme: bool = True):
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


if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
