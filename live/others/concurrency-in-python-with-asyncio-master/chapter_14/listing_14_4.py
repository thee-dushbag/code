import asyncio, uvloop


async def connected(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    line = await reader.readline()
    writer.write(line)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(connected, port=9000)
    await server.serve_forever()


if __name__ == "__main__":
    try:
        uvloop.run(main())
    except KeyboardInterrupt:
        ...
