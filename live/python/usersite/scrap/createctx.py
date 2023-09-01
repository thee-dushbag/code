class CreateContext:
    def __init__(self, enter_, exit_, handler = None) -> None:
        self.enter = enter_
        self.exit = exit_
        self.handler = handler
    
    def __enter__(self):
        return self.enter()
    
    def __exit__(self, *a, **k):
        if self.handler:
            self.handler(*a, **k)
        return self.exit()

    async def __aenter__(self):
        return await self.enter()
    
    async def __aexit__(self, *a, **k):
        if self.handler:
            await self.handler(*a, **k)
        return await self.exit()
