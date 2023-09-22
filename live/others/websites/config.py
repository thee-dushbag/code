from pathlib import Path
from typing import Any, Callable, ClassVar, Coroutine

from aiohttp import hdrs, web
from aiohttp_mako import template
from attrs import define, field


async def _callback(project, request):
    pass


PROJECT_DESC = "Project Description"
WORKING_DIR = Path.cwd()
TEMPLATE_DIR = WORKING_DIR / "templates"
STATIC_DIR = WORKING_DIR / "static"
PUBLIC_DIR = WORKING_DIR / "public"
ProjectCallback = Callable[["Project", web.Request], Coroutine[Any, Any, None]]
DEFAULT_CALLBACK: ProjectCallback = _callback

_routes_defs: dict[str, Callable] = {
    hdrs.METH_POST: web.post,
    hdrs.METH_GET: web.get,
    hdrs.METH_PUT: web.put,
    hdrs.METH_DELETE: web.delete,
}


async def _project_class(project: "Project", request: web.Request):
    project.context["PROJECT"] = project.__class__


class ProjectNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.project_name = name

    def __str__(self) -> str:
        return f"Project with name {self.project_name} was not found"


@define
class Project:
    project_name: str
    route_path: str
    template_name: str
    description: str = field(default=PROJECT_DESC)
    callback: ProjectCallback = field(default=DEFAULT_CALLBACK)
    method: str = field(default=hdrs.METH_GET, converter=str.upper)
    context: dict = field(factory=dict)
    instances: ClassVar[list["Project"]] = list()

    def __attrs_post_init__(self):
        Project.instances.append(self)

    def handler(self, **kwargs):
        self.context.update(kwargs)

        @template(self.template_name)
        async def _handler(req: web.Request):
            await _project_class(self, req)
            await self.callback(self, req)
            return self.context

        return _handler

    def routedef(self, **kwargs) -> web.AbstractRouteDef:
        creator = _routes_defs[self.method]
        handler, name = self.handler(**kwargs), self.project_name
        return creator(self.route_path, handler, name=name)

    @classmethod
    def get_project(cls, name: str):
        for project in cls.instances:
            if project.project_name == name:
                return project
        raise ProjectNotFound(name)
