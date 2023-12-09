async def application(scope, receive, send):
    # The scope object stores all needed information
    # about a request, from the client address to the headers
    # they sent and many more.
    print(f"Scope: {scope}")
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": ((b"content-type", b"text/html"),),
        }
    )
    await send({"type": "http.response.body", "body": b"ASGI hello!"})
