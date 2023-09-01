import strawberry, typing as ty
from strawberry.extensions import SchemaExtension
from strawberry.permission import BasePermission
from strawberry.types import ExecutionContext, Info


class AlwaysFailPermission(BasePermission):
    message = "You are not authorized"

    def has_permission(
        self, source: ty.Any, info: Info[ty.Any, ty.Any], **kwargs: ty.Any
    ) -> bool:
        return False


class MyExtension(SchemaExtension):
    def get_results(self) -> ty.Dict:
        info = self.execution_context
        return {
            "query": info.query or "",
            "variables": info.variables or {},
            "request_headers": dict(info.context["request"].headers),
        }


@strawberry.type
class DebugInfo:
    num_active_result_handlers: int
    is_connection_init_timeout_task_done: ty.Optional[bool]


class Schema(strawberry.Schema):
    def process_errors(
        self, errors: ty.List, execution_context: ty.Optional[ExecutionContext] = None
    ) -> None:
        import traceback

        traceback.print_stack()
        return super().process_errors(errors, execution_context)
