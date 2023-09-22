import typing as ty

import strawberry as straw
from strawberry.types import ExecutionContext


class Schema(straw.Schema):
    def process_errors(
        self, errors: ty.List, execution_context: ty.Optional[ExecutionContext] = None
    ) -> None:
        import traceback

        traceback.print_stack()
        return super().process_errors(errors, execution_context)
