from aiohttp import web
import dataapp.config as cfg, dataapp.dataplugin
from .security import setup as security_setup
from .views import setup as views_setup

_Persisters: dict[str, dataapp.dataplugin.Persister] = {
    "yaml": dataapp.dataplugin.YamlPersister,
    "json": dataapp.dataplugin.JsonPersister,
}


async def application():
    app = web.Application()
    Persister = _Persisters[cfg.PERSIST_TYPE]
    persister = Persister(cfg.USERSDATA_FILE)
    dataapp.dataplugin.setup(app, persister)
    views_setup(app)
    security_setup(app)
    return app
