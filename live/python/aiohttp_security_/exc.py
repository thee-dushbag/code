class DBError(Exception):
    ...

class DBSearch(DBError):
    def __init__(self, target, found=None) -> None:
        self.found = found
        self.target = target

class DBSearchFound(DBSearch):
    ...

class DBSearchNotFound(DBSearch):
    ...

class DBResourceError(DBError):
    def __init__(self, resrc=None) -> None:
        self.resource = resrc

class DBResourceNotYours(DBResourceError):
    ...