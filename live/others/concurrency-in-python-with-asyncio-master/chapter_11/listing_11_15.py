import asyncio as aio, enum


class ConnectionState(enum.Enum):
    WAIT_INIT = enum.auto()
    INITIALIZING = enum.auto()
    INITIALIZED = enum.auto()


class Connection:
    def __init__(self):
        self._state = ConnectionState.WAIT_INIT
        self._condition = aio.Condition()

    async def initialize(self):
        await self._change_state(ConnectionState.INITIALIZING)
        print("initialize: Initializing connection...")
        await aio.sleep(3)  # simulate connection startup time
        print("initialize: Finished initializing connection")
        await self._change_state(ConnectionState.INITIALIZED)

    async def execute(self, query: str):
        async with self._condition:
            print("execute: Waiting for connection to initialize")
            await self._condition.wait_for(self._is_initialized)
            print(f"execute: Running {query!r}")
            await aio.sleep(3)  # simulate a long query

    async def _change_state(self, state: ConnectionState):
        async with self._condition:
            print(f"change_state: State changing from {self._state} to {state}")
            self._state = state
            self._condition.notify_all()

    def _is_initialized(self):
        if self._state is not ConnectionState.INITIALIZED:
            print(
                f"_is_initialized: Connection not finished initializing, state is {self._state}"
            )
            return False
        print(f"_is_initialized: Connection is initialized!")
        return True


async def main():
    connection = Connection()
    query_one = aio.create_task(connection.execute("select * from table"))
    query_two = aio.create_task(connection.execute("select * from other_table"))
    aio.create_task(connection.initialize())
    await query_one
    await query_two


if __name__ == "__main__":
    aio.run(main())
