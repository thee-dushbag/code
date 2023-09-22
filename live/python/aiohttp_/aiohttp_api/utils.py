import bcrypt
import model as md
from sqlalchemy import exc


def hash_password(password: str) -> str:
    bpass = password.encode()
    salt = bcrypt.gensalt()
    hpass = bcrypt.hashpw(bpass, salt)
    return hpass.decode()


def check_password(password: str, hashed: str) -> bool:
    bpass = password.encode()
    hpass = hashed.encode()
    _e = bcrypt.checkpw(bpass, hpass)
    return _e


def _end_session(session, *excs):
    excs = excs or (Exception,)
    try:
        session.commit()
    except excs as e:
        session.rollback()
        return False
    else:
        return True


def add_user(session, username: str, password: str):
    hpass = hash_password(password)
    user = md.User(name=username, password=password)
    session.add(user)
    return _end_session(session)
