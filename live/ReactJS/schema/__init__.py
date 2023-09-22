from ._schema import Schema
from .mutation import Mutation
from .query import Query
from .subscription import Subscription

__all__ = "Query", "Subscription", "Mutation", "schema", "Schema"

schema = Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,  # , extensions=[MyExtension]
)
