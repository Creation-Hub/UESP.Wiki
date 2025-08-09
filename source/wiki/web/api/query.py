import json
import logging
import requests
from enum import Enum
from http import HTTPStatus
from typing import Any
from requests import Response
from ..site import Site
from .main import Main
from .actions import Action
from .data import DataFormat


class QueryParameter(str, Enum):
    META = "meta"


class Query:
    JSON_INDENT:int = 2

    @staticmethod
    def info(site:Site) -> str:
        """Get basic wiki information"""
        parameters:dict[str, str] = {
            Main.ACTION: Action.QUERY,
            Main.FORMAT: DataFormat.JSON,
            QueryParameter.META: "siteinfo"
        }
        response:Response = requests.get(site.api_url, params=parameters)
        if response.status_code == HTTPStatus.OK:
            data:Any = response.json()
            dump:str = json.dumps(data, indent=Query.JSON_INDENT)
            return dump
        else:
            logging.error(f"Failed to get site info: Status {response.status_code}")
            return ""
