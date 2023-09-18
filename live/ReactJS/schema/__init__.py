from .query import Query
from .mutation import Mutation
from .subscription import Subscription
from ._schema import Schema

__all__ = 'Query', 'Subscription', 'Mutation', 'schema', 'Schema'

schema = Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,  # , extensions=[MyExtension]
)