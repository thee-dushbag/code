import json
import os
from itertools import count
from pathlib import Path
from typing import Any, ClassVar, cast

from aiohttp import web
from attrs import asdict, define, field

routes = web.RouteTableDef()
todos: list["Todo"] = []
START = 0
counter = count(START)
todoid = lambda: next(counter)
file = Path("./todos.json")
if not file.exists():
    file.touch()
    j = json.dumps({"todos": []})
    file.write_text(j)


def save_todos(*_, **__):
    t = [asdict(e) for e in todos]
    j = json.dumps({"todos": t})
    file.write_text(j)


def load_todos(*_, **__):
    global todos, counter
    j = json.loads(file.read_text())
    todos = [Todo(**g) for g in j["todos"]]  # type: ignore
    counter = count(max((START, *(x.todo_id for x in todos))) + bool(todos))  # type: ignore


def consume_app(func):
    async def consume(*_, **__):
        func()

    return consume


@define
class Todo:
    title: str
    desc: str
    todo_id: int = field(factory=todoid)


def create_todo(data: dict[str, str | Any]):
    title = data.get("title", None)
    desc = data.get("desc", None)
    if title and desc:
        return Todo(title, desc)
    return None


@routes.get("/todos")
async def get_todos(req: web.Request):
    offset = req.query.get("offset", "0")
    limit = req.query.get("limit", str(len(todos)))
    _e = web.HTTPBadRequest(reason=f"Invalid: {offset=} or {limit=}")
    if not offset.isnumeric():
        raise _e
    if not limit.isnumeric():
        raise _e
    offset, limit = map(lambda i: abs(int(i)), (offset, limit))
    end = limit + offset
    ltodos = tuple(asdict(t) for i, t in enumerate(todos) if i >= offset and i < end)
    return web.json_response(ltodos)


@routes.post("/todos")
async def add_todo(req: web.Request):
    data = cast(dict, await req.post())
    if todo := create_todo(data):
        todos.append(todo)
        return web.json_response(asdict(todo))
    raise web.HTTPBadRequest(reason="Error Creating Todo")


@routes.delete("/todos")
async def delete_todo(req: web.Request):
    todo_id = req.query.get("todo_id", "")
    _e = web.HTTPBadRequest(reason=f"Invalid todo_id: {todo_id!r}")
    if not todo_id or not todo_id.isnumeric():
        raise _e
    tid, target = int(todo_id), None

    def get_target(todo: Todo):
        if not todo.todo_id == tid:
            return 1
        nonlocal target
        target = todo

    global todos
    todos = list(filter(get_target, todos))
    if target is None:
        raise _e
    return web.json_response(asdict(target))


@routes.put("/todos")
async def edit_todo(req: web.Request):
    todo_id = req.query.get("todo_id", "")
    _e = web.HTTPBadRequest(reason=f"Invalid todo_id: {todo_id!r}")
    if not todo_id or not todo_id.isnumeric():
        raise _e
    tid, target = int(todo_id), None

    def get_target(todo: Todo):
        if todo.todo_id == tid:
            nonlocal target
            target = todo

    for todo in todos:
        get_target(todo)
    if target is None:
        raise _e
    data = await req.post()
    if "title" in data:
        target.title = data["title"]
    if "desc" in data:
        target.desc = data["desc"]
    return web.json_response(asdict(target))


app = web.Application()
app.on_startup.append(consume_app(load_todos))
app.on_shutdown.append(consume_app(save_todos))
app.add_routes(routes)
