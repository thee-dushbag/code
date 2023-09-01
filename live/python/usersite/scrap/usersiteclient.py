from dataclasses import asdict, dataclass
from typing import cast
from httpx import AsyncClient
import re


@dataclass
class User:
    name: str
    password: str
    email: str


@dataclass(kw_only=True)
class UserSiteConfig:
    login_url: str
    signup_url: str
    base_url: str
    delete_url: str
    logout_url: str
    cpword_url: str
    invalid_uid: int = -1


class UserSiteClient:
    def __init__(self, config: UserSiteConfig, user: User):
        self.user: User = user
        self.config = config
        self.session: AsyncClient | None = None
        self.user_id: int = self.config.invalid_uid

    async def __aenter__(self):
        if self.session is None:
            self.session = await self.create_session()
        return self

    def get_userid(self, user_url: str) -> int:
        mat = re.compile(r"^/user/(?P<uid>\d+)$").match(user_url)
        return int(mat.group("uid")) if mat else self.config.invalid_uid

    async def create_session(self):
        return AsyncClient(base_url=self.config.base_url, follow_redirects=True)

    @property
    def connected(self) -> bool:
        return self.session is not None

    async def login(self):
        if self.connected:
            self.session = cast(AsyncClient, self.session)
            page = await self.session.post(
                self.config.login_url, data=asdict(self.user)
            )
            self.user_id = self.get_userid(page.url.path)
            return page

    async def logout(self):
        if self.connected and self.logged_in:
            self.session = cast(AsyncClient, self.session)
            page = await self.session.get(self.config.logout_url.format(self.user_id))
            self.user_id = self.config.invalid_uid
            return page


    async def signup(self):
        if self.connected:
            self.session = cast(AsyncClient, self.session)
            return await self.session.post(
                self.config.signup_url, data=asdict(self.user)
            )

    async def delete(self):
        if self.connected and self.logged_in:
            self.session = cast(AsyncClient, self.session)
            page = await self.session.get(self.config.delete_url.format(self.user_id))
            self.user_id = self.config.invalid_uid
            return page

    async def change_password(self, new_password: str):
        if self.connected and self.logged_in:
            self.session = cast(AsyncClient, self.session)
            ps = dict(old_password=self.user.password, new_password=new_password)
            page = await self.session.post(
                self.config.cpword_url.format(self.user_id), data=ps
            )
            self.user.password = new_password
            return page

    async def __aexit__(self, *_):
        if self.session:
            await self.session.aclose()
            self.session = None

    @property
    def logged_in(self) -> bool:
        return self.user_id != self.config.invalid_uid
