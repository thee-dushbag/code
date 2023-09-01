from strawberry.aiohttp.handlers import GraphQLTransportWSHandler, GraphQLWSHandler


class DebuggableGraphQLTransportWSHandler(GraphQLTransportWSHandler):
    def get_tasks(self) -> list:
        return [op.task for op in self.operations.values()]

    async def get_context(self) -> object:
        context = await super().get_context()
        context["ws"] = self._ws
        context["get_tasks"] = self.get_tasks
        context["connectionInitTimeoutTask"] = self.connection_init_timeout_task
        return context


class DebuggableGraphQLWSHandler(GraphQLWSHandler):
    def get_tasks(self) -> list:
        return list(self.tasks.values())

    async def get_context(self) -> object:
        context = await super().get_context()
        context["ws"] = self._ws
        context["get_tasks"] = self.get_tasks
        context["connectionInitTimeoutTask"] = None
        return context
