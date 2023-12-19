import asyncio as aio


class MockSocket:
    def __init__(self):
        self.socket_closed = False

    async def send(self, msg: str):
        if self.socket_closed:
            raise Exception("Socket is closed!")
        print(f"Sending: {msg}")
        await aio.sleep(1)
        print(f"Sent: {msg}")

    def close(self):
        self.socket_closed = True


users2sockets = {
    "John": MockSocket(),
    "Terry": MockSocket(),
    "Graham": MockSocket(),
    "Eric": MockSocket(),
}


async def user_disconnect(username: str, user_lock: aio.Lock):
    print(f"{username} disconnected!")
    async with user_lock:  # A
        print(f"Removing {username} from chat")
        socket = users2sockets.pop(username)
        socket.close()


async def message_all_users(user_lock: aio.Lock):
    print("Creating message tasks")
    async with user_lock:  # B
        messages = (
            socket.send(f"Hello {user}") for user, socket in users2sockets.items()
        )
        await aio.gather(*messages)



async def main():
    user_lock = aio.Lock()
    await aio.gather(message_all_users(user_lock), user_disconnect("Eric", user_lock))


if __name__ == "__main__":
    aio.run(main())
