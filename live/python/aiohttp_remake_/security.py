from aiohttp_security.abc import AbstractAuthorizationPolicy
from model_helpers import DatabaseManager

class NoteAppAuthPolicy(AbstractAuthorizationPolicy):
    def __init__(self, manager: DatabaseManager) -> None:
        self.manager = manager
    
    async def authorized_userid(self, identity):
        return self.manager.get_user_by_name(identity)
    
    async def permits(self, identity, permission, context=None):
        return True