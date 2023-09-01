from functools import partial
from pathlib import Path
from attrs import define, field
from aiohttp import web
import json

APP_KEY = 'data.app_key.attrs.Data.aiohttp.store'

@define
class Data:
    store: Path = field()
    data: dict = field(factory=dict)

    def __attrs_post_init__(self):
        if not self.store.exists():
            self.store.touch()
        assert self.store.is_file()

    def __enter__(self):
        self.load()
        return self
    
    def __exit__(self, *exc):
        self.save()

    def fresh(self):
        current = self.data
        self.load()
        self.data = {**current, **self.data}
        self.save()

    def load(self):
        content = self.store.read_text() or "{}"
        self.data = json.loads(content)

    def save(self):
        self.store.write_text(json.dumps(self.data, indent=2))

def get_app_data(app: web.Application) -> Data:
    if data := app.get(APP_KEY, None):
        return data
    raise Exception("Data was not setup")

def get_data(req: web.Request):
    return get_app_data(req.app)

class _DataView(web.View):
    def __init__(self, request: web.Request) -> None:
        super().__init__(request)
        self.data = get_data(request)

async def data_ctx(app: web.Application, path: Path, init=None):
    with Data(path, init or dict()) as data:
        app[APP_KEY] = data
        yield

def setup(app: web.Application, path: Path, init = None):
    datactx = partial(data_ctx, path=path, init=init)
    app.cleanup_ctx.append(datactx)