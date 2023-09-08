import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()

print(f"Listening on: tcp://{':'.join(map(str, server_address))}")

connection, client_address = server_socket.accept()
data = connection.recv(1024)
connection.send(b'Hello, Welcome! I am closing now, GoodBye.')
print(f'I got a connection from {client_address}!')
print(f"Client said: {data.decode()!r}")
server_socket.close()
