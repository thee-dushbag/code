from aiohttp import web
from config import Project


async def index(project: Project, request: web.Request):
    project.context["projects"] = project.instances
