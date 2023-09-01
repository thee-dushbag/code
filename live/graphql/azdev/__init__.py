from ._base import DebuggableGraphQLTransportWSHandler, DebuggableGraphQLWSHandler
from strawberry.aiohttp.views import GraphQLView
from .subsription import Subscription
from .db import setup as db_setup
from .mutation import Mutation
from aiohttp import web, hdrs
from ._schema import Schema
from .query import Query

class MyGraphQLView(GraphQLView):
    graphql_transport_ws_handler_class = DebuggableGraphQLTransportWSHandler
    graphql_ws_handler_class = DebuggableGraphQLWSHandler

    async def get_root_value(self, request: web.Request) -> Query:
        await super().get_root_value(request)  # for coverage
        return Query()

_schema = Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)

def setup(app: web.Application,* , prefix: str = '/azdev/api', **kwargs):
    endpoint = MyGraphQLView(_schema, **kwargs)
    app.router.add_route(hdrs.METH_ANY, prefix, endpoint)
    return db_setup(app)