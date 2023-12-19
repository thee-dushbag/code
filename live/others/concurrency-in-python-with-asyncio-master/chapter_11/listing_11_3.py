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


async def user_disconnect(username: str):
    print(f"{username} disconnected!")
    socket = users2sockets.pop(username)
    socket.close()


async def message_all_users():
    print("Creating message tasks")
    messages = (socket.send(f"Hello {user}") for user, socket in users2sockets.items())
    await aio.gather(*messages)


async def main():
    # Okay:
    # await aio.gather(user_disconnect("Eric"), message_all_users())
    # Fails:
    await aio.gather(message_all_users(), user_disconnect("Eric"))


if __name__ == "__main__":
    aio.run(main())
