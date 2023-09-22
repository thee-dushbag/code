from enum import Enum
from typing import Any


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
