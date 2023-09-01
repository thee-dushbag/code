from sqlalchemy.orm import Session as _Session
from model import User
from exc import OperationStatus, OpType, State
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound

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
            self.session.rollback()
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
                if val: setattr(user, key, val)
            self.session.add(user)
            self.session.commit()
        except (MultipleResultsFound, NoResultFound, IntegrityError) as e:
            self.session.rollback()
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
                self.session.commit()
        except (MultipleResultsFound, NoResultFound) as e:
            self.session.rollback()
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
            self.session.rollback()
            state = State.FAILURE
            message = str(e)
        else:
            state = State.SUCCESS
            message = "Found UserID"
        return OperationStatus(optype, state, message, result=userid)

