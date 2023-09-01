import atexit
import asyncio as aio
from typing import Sequence
from dataclasses import asdict
from faker import Faker
from createctx import CreateContext
from utils import get_welcome, save_all, create_user, load_users
from usersiteclient import UserSiteClient, UserSiteConfig, User

USERS_FILENAME = "users.json"
users: list[dict] = load_users(USERS_FILENAME)


async def delete_user(client: UserSiteClient):
    await client.delete()
    global users

    def is_deleted(user):
        return user["name"] != client.user.name

    users = list(filter(is_deleted, users))


async def add_user(fake=None):
    global users, usersite_config
    _fake = fake or Faker()
    user = await create_user(_fake)
    users.append(asdict(user))
    async with UserSiteClient(usersite_config, user) as client:
        await client.signup()
    return client


atexit.register(
    lambda: save_all(
        USERS_FILENAME, dict(users=globals().get("users", [])), overwrite=True
    ),
)

PORT = 5052
HOST = "localhost"
USER_URL = "/user/{}"
LOGIN_URL = "/login_post"
SIGNUP_URL = "/signup_post"
DELETE_URL = "/delete_post/{}"
CPWORD_URL = "/cpword_post/{}"
LOGOUT_URL = "/logout/{}"
BASE_URL = f"http://{HOST}:{PORT}"


usersite_config = UserSiteConfig(
    login_url=LOGIN_URL,
    logout_url=LOGOUT_URL,
    signup_url=SIGNUP_URL,
    delete_url=DELETE_URL,
    base_url=BASE_URL,
    cpword_url=CPWORD_URL,
)


async def main(argv: Sequence[str]) -> None:
    for user in users:
        async with UserSiteClient(usersite_config, User(**user)) as uclient:
            async with CreateContext(uclient.login, uclient.logout) as page:
                print(await get_welcome(page.content.decode()))
                await delete_user(uclient)
    #for i in range(10):
    #    async with await add_user() as uclient:
    #        async with CreateContext(uclient.login, uclient.logout) as page:
    #                print(await get_welcome(page.content.decode()))


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
