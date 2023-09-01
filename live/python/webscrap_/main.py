from typing import Sequence
from store import CloudStore, CloudStoreURL
import cfg, asyncio as aio
from mpack import print

USERNAME = "simon_nganga"
PASSWORD = 'simonPassword5052Secret'

store_url = CloudStoreURL(
    add_user=cfg.ADDUSER_URL.path,
    rm_user=cfg.RMUSER_URL.path,
    store_url=cfg.STORE_URL.path,
    base_url=cfg.BASE_URL.__str__()
)

async def test_create_delete(store: CloudStore):
    print("Cloud Setup Complete")
    if not await store.have_account():
        print("No Account: Creating One")
        if await store.create_account():
            print(f"Account created Successfully for {USERNAME}")
        else:
            print(f"Account creation for {USERNAME} Failed")
    else:
        print("Acount Found: Unexpected")
    print("Using Account")
    await aio.sleep(3)
    print("Acount Operations Complete")
    if await store.have_account():
        print("Account Found: Deleting Account")
        if await store.delete_account():
            print(f"Deleting Account for {USERNAME} Successful")
        else:
            print(f"Deleting Account for {USERNAME} Failed")
    else:
        print("No Acount Found: Unexpected")

async def main(argv: Sequence[str]) -> None:
    store = CloudStore(store_url, USERNAME, PASSWORD)
    if not await store.have_account():
        if not await store.create_account():
            print("Account Creation Error")
            exit(-1)
    t1 = store.update('name', 'Simon Nganga Njoroge')
    t2 = store.update_all({
        'age': 22,
        'single': False,
        'school': 'Chuka University'
    })
    await aio.gather(t1, t2)
    await store.ensure_store('name', 'Faith Njeri Wanjiru')
    await store.ensure_store('NAME', 'Lydia Njeri Wanjiru')
    await store.delete_all()
    await store.delete_account()



if __name__ == '__main__':
    from sys import argv
    aio.run(main(argv[1:]))