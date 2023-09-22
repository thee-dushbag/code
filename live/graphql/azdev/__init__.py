from aiohttp import hdrs, web
from strawberry.aiohttp.views import GraphQLView

from ._base import (DebuggableGraphQLTransportWSHandler,
                    DebuggableGraphQLWSHandler)
from ._schema import Schema
from .db import setup as db_setup
from .mutation import Mutation
from .query import Query
from .subsription import Subscription


class MyGraphQLView(GraphQLView):
    graphql_transport_ws_handler_class = DebuggableGraphQLTransportWSHandler
    graphql_ws_handler_class = DebuggableGraphQLWSHandler

    async def get_root_value(self, request: web.Request) -> Query:
        await super().get_root_value(request)  # for coverage
        return Query()


_schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)


def setup(app: web.Application, *, prefix: str = "/azdev/api", **kwargs):
    endpoint = MyGraphQLView(_schema, **kwargs)
    app.router.add_route(hdrs.METH_ANY, prefix, endpoint)
    return db_setup(app)
