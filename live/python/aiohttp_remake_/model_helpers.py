import enum

import bcrypt as _bc
from aiohttp import web
from model import APP_KEY as MODEL_APP_KEY
from model import DatabaseModel, Note, User
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound

FORMAT = "utf-8"


class AccessRight(enum.IntEnum):
    PRIVATE = enum.auto()
    PUBLIC = enum.auto()


def hash_password(password: str) -> str:
    bpass = password.encode(FORMAT)
    hpass = _bc.hashpw(bpass, _bc.gensalt())
    return hpass.decode(FORMAT)


def check_password(password: str, hashed: str) -> bool:
    hpass = hashed.encode(FORMAT)
    bpass = password.encode(FORMAT)
    return _bc.checkpw(bpass, hpass)


class DatabaseManager:
    def __init__(self, db: DatabaseModel) -> None:
        self.session = db.create_session()
        self.db = db

    def check_credentials(self, name: str, password: str = "") -> bool:
        user = self.get_user_by_name(name)
        if user is None:
            return False
        hpassword = str(user.password)
        return check_password(password, hpassword)

    def get_user_by_name(self, name: str) -> User | None:
        try:
            return self.session.query(User).where(User.name == name).one()
        except NoResultFound as error:
            ...

    def get_user_by_id(self, user_id: int) -> User | None:
        try:
            return self.session.query(User).where(User.user_id == user_id).one()
        except NoResultFound as error:
            ...

    def add_user(self, name: str, password: str, email: str):
        hashed = hash_password(password)
        user = User(name=name, password=hashed, email=email)
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return False
        else:
            return True

    def add_note(self, note: Note):
        self.session.add(note)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return False
        else:
            return True

    def get_note_by_id(self, note_id: int) -> Note | None:
        try:
            return self.session.query(Note).where(Note.note_id == note_id).one()
        except NoResultFound:
            ...

    def delete_note(self, note_id: int):
        note = self.get_note_by_id(note_id)
        if note is None:
            return
        self.session.delete(note)
        self.session.commit()
        return True

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user is None:
            return
        self.session.delete(user)
        self.session.commit()
        return True


def get_all_user_notes(db: DatabaseManager, user_id: int):
    return db.session.query(Note).where(Note.user_id == user_id)


def get_all_user_private_notes(db: DatabaseManager, user_id: int):
    return get_all_user_notes(db, user_id).filter(Note.access_id == AccessRight.PRIVATE)


def get_all_user_public_notes(db: DatabaseManager, user_id: int):
    return get_all_user_notes(db, user_id).filter(Note.access_id == AccessRight.PUBLIC)


def manager_from_request(req: web.Request):
    db: DatabaseModel = req.app.get(MODEL_APP_KEY, None)
    if db is None:
        text = "initialize database with model.setup(app, ...)"
        raise KeyError(text)
    return DatabaseManager(db)
