from config import Project
from aiohttp import web

async def index(project: Project, request: web.Request):
    project.context['projects'] = project.instances.values()
