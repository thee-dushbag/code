from aiohttp import web
from . import config as cfg, dataplugin as dp
from .security import setup as security_setup
from .views import setup as views_setup

_Persisters: dict[cfg.PersistTypes, type[dp.Persister]] = {
    "yaml": dp.YamlPersister,
    "json": dp.JsonPersister,
}


async def application():
    app = web.Application()
    Persister = _Persisters[cfg.PERSIST_TYPE]
    persister = Persister(cfg.USERSDATA_FILE)
    dp.setup(app, persister)
    views_setup(app)
    security_setup(app)
    return app
