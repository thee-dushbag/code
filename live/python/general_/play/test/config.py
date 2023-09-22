from typing import Mapping, MutableMapping

import exc
from aiohttp import web
from utils import Config

CONFIG_KEY = "app.base_config.config"


def _get_config(config_map: Mapping, config_key: str):
    if config := config_map.get(config_key, None):
        return config
    raise exc.ConfigNotFound(config_key, config)


def get_config(conig_map: Mapping, config_key: str) -> Config:
    base_config = _get_config(conig_map, CONFIG_KEY)
    return _get_config(base_config, config_key)


def _add_config(base_config: MutableMapping, config: Config):
    config_key = config._config_key
    if conf := base_config.get(config_key):
        raise exc.ConfigFound(config_key, conf)
    base_config.setdefault(config_key, config)


def setup(app: web.Application, config_registry: list[Config]):
    base_config = app.setdefault(CONFIG_KEY, Config(CONFIG_KEY))
    for config in config_registry:
        _add_config(base_config, config)
    return base_config
