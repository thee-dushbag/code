import asyncio
import logging as log
import socket as sock
from asyncio import AbstractEventLoop, CancelledError
from socket import socket

log.basicConfig(level=log.INFO)
echos = []


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            if data == b"boom\r\n":
                raise Exception("Boom: Network Error")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        log.error(f"Echo Error: {str(ex)!r}")
    finally:
        connection.close()
        log.info(f"Connection Closed.")


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    try:
        while True:
            connection, address = await loop.sock_accept(server_socket)
            connection.setblocking(False)
            log.info(f"Got a connection from {address}")
            t = asyncio.create_task(echo(connection, loop))
            echos.append(t)
    except CancelledError:
        ...


def graceful_shutdown():
    for task in echos:
        task.cancel()
    asyncio.get_running_loop().remove_signal_handler(2)
    [task.cancel() for task in asyncio.all_tasks()]


async def main():
    server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server_socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

    server_address = ("127.0.0.1", 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(2, graceful_shutdown)

    with server_socket:
        await listen_for_connection(server_socket, loop)
    log.info("Application closing.")


asyncio.run(main())
