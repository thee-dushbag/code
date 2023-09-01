# type: ignore

from typing import Callable, Any
from mypyutils.encrypt import Encripter


def get_keys(text: str, tkdlm: str = "|", dlm: str = "@") -> dict[str, str]:
    tokens = text.split(tkdlm)
    res = dict()
    for token in tokens:
        key, value = token.split(dlm)
        res[key] = value
    return res


def merge_str(data: dict[Any, Any], tkdlm: str = "|", dlm="@") -> str:
    tokens: list[str] = [f"{key}{dlm}{value}" for key, value in data.items()]
    return tkdlm.join(tokens)


class Client:
    def __init__(self, name: str, server: "Server|None" = None) -> None:
        self.name: str = name
        self.server = server

    def set_server(self, server: "Server") -> None:
        self.server = server

    def onReceive(self, msg: str) -> None:
        print(f"Received: {msg!r}")
        msg = server.encrypter.decrypt(msg)
        data: dict[str, str] = get_keys(msg)
        name, msg = data["name"], data["msg"]
        print(f"\x1b[91;1m{self.name} \x1b[97;1mrecv:\x1b[92;1m {name}: {msg}\x1b[0m")

    def send(self, msg: str) -> None:
        print(f"\x1b[94;1m{self.name} \x1b[97;1msent:\x1b[93;1m {msg}\x1b[0m")
        self.server.send(
            self, server.encrypter.encrypt(merge_str({"name": self.name, "msg": msg}))
        )

    def quit(self):
        self.server.send(self, self.server.encrypter.encrypt(merge_str({"quit": True})))
        self.server.rm_client(self)
        self.server = None

    def __eq__(self, client: "Client") -> bool:
        return self.name == client.name

    def __ne__(self, client: "Client") -> bool:
        return not self == client

    def __str__(self) -> str:
        return f"<Client(name='{self.name}')>"


class Server:
    def __init__(
        self,
        options: dict[str, Callable] | None = None,
        *clients: Client,
        encrypter: Encripter = Encripter(),
    ) -> None:
        self.clients: list[Client] = list(clients)
        self.options = options if options else dict()
        self.encrypter = encrypter

    def add_option(
        self, key: str, call: Callable[["Server", "Client", str], Any]
    ) -> None:
        self.options[key] = call

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def broadcast_msg(self, sender: Client, msg: str) -> None:
        msg = self.encrypter.encrypt(msg)
        for client in self.clients:
            if client != sender:
                client.onReceive(msg)

    def parse(self, key, value, client):
        if func := self.options.get(key):
            func(self, client, value)

    def rm_client(self, client: Client) -> None:
        self.clients = [clt for clt in self.clients if clt != client]
        self.broadcast_msg(
            client,
            merge_str({"msg": f"{client.name} left the group.", "name": "Server"}),
        )

    def send(self, sender: Client, msg: str) -> None:
        msg = self.encrypter.decrypt(msg)
        tokens: dict[str, str] = get_keys(msg)
        for key, value in tokens.items():
            self.parse(key, value, sender)
        if "name" in tokens and "msg" in tokens:
            name, msg = tokens["name"], tokens["msg"]
            self.broadcast_msg(sender, merge_str(dict(name=name, msg=msg)))


def server_say_hi(server: Server, client: Client, value: str) -> None:
    server.broadcast_msg(
        client, merge_str(dict(name="Server", msg=f"Hello {value}, how was your day?"))
    )


def remove_me(server: Server, client: Client, value: str) -> None:
    server.rm_client(client)
    server.broadcast_msg(
        client,
        merge_str(
            dict(
                name="Server",
                msg=f'I fucking did removed {client.name} and said "{value}"',
            )
        ),
    )


def kick_someone(server: Server, client: Client, value: str) -> None:
    i = -1
    for index, clt in enumerate(server.clients):
        if clt.name == client.name:
            i = index
        if clt.name == value:
            i = index
    server.broadcast_msg(
        client,
        merge_str(
            dict(
                name="Server", msg=f"{client.name} requested {value} to be kicked off."
            )
        ),
    )
    server.rm_client(server.clients[i])


if __name__ == "__main__":
    names: list[str] = ["Simon", "Mark", "John", "Joseph", "Shiro"]
    server = Server()
    server.add_option("server_say_hi", server_say_hi)
    server.add_option("remove_me", remove_me)
    server.add_option("kick", kick_someone)
    clients: list[Client] = [Client(name, server) for name in names]
    [server.add_client(client) for client in clients]
    msgs: list[str] = [
        "Hello everyone?",
        "Hi?",
        "Hi tew|kick@Joseph",
        "Niko Poa, fucker.|remove_me@Fuck every one in here, y'all are losers.",
        "A we kufa.|server_say_hi@Simon",
    ]
    for index, msg in enumerate(msgs):
        clients[index].send(msg)
