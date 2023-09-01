from typing import TYPE_CHECKING
from exc import OperationStatus, OpType, State
import bcrypt
from typing import cast
from usermanager import UserManager
from model import User

USERSITE = 'USERSITE'


class UserSite:
    def __init__(self, manager: UserManager, format_: str) -> None:
        self.logged_in: dict[str, User] = {}
        self.manager = manager
        self.format = format_

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        bpass = password.encode(self.format)
        epass = bcrypt.hashpw(bpass, salt)
        return epass.decode(self.format)

    def _check_password(self, userpw: str, hashedpw: str) -> bool:
        upass = userpw.encode(self.format)
        hpass = hashedpw.encode(self.format)
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
