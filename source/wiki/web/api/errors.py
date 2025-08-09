"""
https://www.mediawiki.org/wiki/API:Errors_and_warnings
"""
from enum import Enum
from typing import Any
from requests import Response
from .responses import ResponseType


class ErrorFormat(str, Enum):
    """
    https://www.mediawiki.org/wiki/API:Errors_and_warnings#Errors
    """
    HTML = "html"
    WIKI = "wikitext"
    TEXT = "plaintext"
    RAW  = "raw"
    NONE = "none"


class ErrorType(str, Enum):
    TYPE = "error"
    CODE = "code"
    INFO = "info"
    EXTRA = "*"


class ErrorCode(str, Enum):
    RATE_LIMITED = "ratelimited"
    """You've exceeded your rate limit. Please wait some time and try again."""


class ResponseError(ResponseType):
    def __init__(self, response:Response) -> None:
        super().__init__(response)

        self.code:str|None = None
        """The error code returned by the API."""

        self.info:str|None = None
        """Additional information about the error."""

        self.extra:Any|None = None
        """Extra information about the error, if available."""
