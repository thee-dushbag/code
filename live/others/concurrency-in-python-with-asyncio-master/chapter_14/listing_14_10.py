import functools, selectors, socket
from listing_14_8 import CustomFuture


def accept_connection(future: CustomFuture):  # A
    def getsocket(connection: socket.socket):
        print(f"We got a connection from {connection}!")
        future.set_result(connection)

    return getsocket


async def sock_accept(sel: selectors.BaseSelector, sock) -> socket.socket:  # B
    print("Registering socket to listen for connections")
    future: CustomFuture[socket.socket] = CustomFuture()
    sel.register(sock, selectors.EVENT_READ, accept_connection(future))
    print("Pausing to listen for connections...")
    return await future


async def main(sel: selectors.BaseSelector):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("127.0.0.1", 8000))
    sock.listen()
    sock.setblocking(False)

    print("Waiting for socket connection!")
    connection = await sock_accept(sel, sock)  # C
    print(f"Got a connection {connection}!")


selector = selectors.DefaultSelector()

coro = main(selector)

while True:  # D
    try:
        state = coro.send(None)
        events = selector.select()

        for key, mask in events:
            print("Processing selector events...")
            print(mask)
            callback = key.data
            callback(key.fileobj)
    except StopIteration as si:
        print("Application finished!")
        break
