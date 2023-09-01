from typing import Any

class AppError(Exception):
    'All Exceptions for this App.'

class SettingsError(AppError):
    'Settings Errors.'

class ConfigError(SettingsError):
    'Config Errors.'
    def __init__(self, config_key: str, config=None, *args: object) -> None:
        super().__init__(*args)
        self.config_key = config_key
        self.config = config
    
    def __str__(self) -> str:
        clsname = self.__class__.__name__
        return f'{clsname}: {self.config_key} -> {self.config}'

class ConfigFound(ConfigError):
    'Error if config already exists.'

class ConfigNotFound(ConfigError):
    'Error if config was not found.'

class ConfigKeyNotFound(ConfigError):
    'Error thrown by getattr when config key is not found'

class MISSING_VALUE(object):
    'Missing value placeholder sentinel'
    def __call__(self, *_, **__): return self
    def __setattr__(self, *_, **__): return self
    def __getattr__(self, *_, **__): return self
    def __getitem__(self, *_, **__): return self
    def __setitem__(self, *_, **__): return self
    def __delitem__(self, *_, **__): return self
    def __get__(self, *_, **__): return self
    def __set__(self, *_, **__): return self
    def __delete__(self, *_, **__): return self

_MISSING = MISSING_VALUE()
