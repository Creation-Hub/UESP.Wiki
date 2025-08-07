import logging
from enum import Enum
from typing import Any

class LogLevel(int, Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


    @staticmethod
    def json_decode(data:dict[str, Any], property:str) -> 'LogLevel|None':
        value:Any = data.get(property, None)
        return LogLevel.convert(value)


    @staticmethod
    def convert(value:Any) -> 'LogLevel|None':
        if isinstance(value, int):
            return LogLevel(value)
        elif isinstance(value, str):
            value = value.upper()
            return LogLevel[value]
        else:
            return None
