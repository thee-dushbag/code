from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TEMPLATE_PATH = Path.cwd() / "templates"
templates = Jinja2Templates(TEMPLATE_PATH)
app = FastAPI(default_response_class=HTMLResponse)


def render_templates(templates: Jinja2Templates):
    def render(name: str):
        def handler(func: Callable[..., Coroutine[Any, Any, dict]]):
            @wraps(func)
            async def handler_args(*args: Any, **kwargs: Any):
                ctx = await func(*args, **kwargs)
                return templates.get_template(name).render(**ctx)

            return handler_args

        return handler

    return render


render = render_templates(templates)


@app.get("/")
# @render('index.html')
async def index(req: Request):
    return templates.TemplateResponse("index.html", dict(request=req))
