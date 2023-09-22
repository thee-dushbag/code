import asyncio as aio
from dataclasses import dataclass
from typing import Any

from httpx import AsyncClient, BasicAuth


@dataclass
class CloudStoreURL:
    add_user: str
    rm_user: str
    store_url: str
    base_url: str


class CloudStore:
    def __init__(self, store_url, username, password) -> None:
        self.urls: CloudStoreURL = store_url
        self.auth = BasicAuth(username, password)
        self.username: str = username
        self.password: str = password
        self.client = AsyncClient(
            base_url=self.urls.base_url, auth=self.auth, follow_redirects=True
        )

    async def create_account(self):
        userauth = dict(username=self.username, password=self.password)
        res = await self.client.post(self.urls.add_user, data=userauth)
        return res.is_success

    async def create(self, key: str, data: Any):
        return await self.create_all({key: data})

    async def create_all(self, keysdata_map: dict):
        res = await self.client.post(self.urls.store_url, json=keysdata_map)
        return res.json()

    async def update(self, key: str, data: Any):
        return await self.update_all({key: data})

    async def update_all(self, keysdata_map: dict):
        res = await self.client.put(self.urls.store_url, json=keysdata_map)
        return res.json()

    async def delete_data(self, key: str):
        res = await self.client.delete(self.urls.store_url, params={"key": key})
        return res.json()

    async def get_data(self, key: str | None = None):
        p = {"key": str(key)} if key else {}
        res = await self.client.get(self.urls.store_url, params=p)
        return res.json()

    async def ensure_store(self, key: str, data: Any):
        edata = await self.get_data()
        target = self.update if key in edata else self.create
        return await target(key, data)

    async def delete_all(self):
        edata = await self.get_data()
        dtasks = (self.delete_data(key) for key in edata)
        return await aio.gather(*dtasks)

    async def have_account(self):
        res = await self.client.get(self.urls.store_url)
        return res.is_success

    async def delete_account(self):
        userauth = dict(username=self.username, password=self.password)
        res = await self.client.post(self.urls.rm_user, data=userauth)
        return res.is_success
