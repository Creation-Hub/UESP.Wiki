import json
import logging
import requests
from enum import Enum
from http import HTTPStatus
from requests import Response
from typing import Any
from ..site import Site
from .actions import Action
from .data import DataFormat
from .main import Main


class ParamInfoParameter(str, Enum):
    MODULES = "modules"


class ParamInfo:

    @staticmethod
    def modules(site:Site) -> str:
        """Get list of available API modules"""
        parameters:dict[str, str] = {
            Main.ACTION: Action.PARAMINFO,
            Main.FORMAT: DataFormat.JSON_FM
        }
        response:Response = requests.get(site.api_url, params=parameters)
        if response.status_code == HTTPStatus.OK:
            data:Any = response.json()
            dump:str = json.dumps(data, indent=2)
            return dump
        else:
            logging.error(f"Failed to get query modules: Status {response.status_code}")
            return ""


    @staticmethod
    def modules_query(site:Site) -> str:
        """Get available query modules (what you can query for)"""
        parameters:dict[str, str] = {
            Main.ACTION: Action.PARAMINFO,
            Main.FORMAT: DataFormat.JSON_FM,
            ParamInfoParameter.MODULES: "query"
        }
        response:Response = requests.get(site.api_url, params=parameters)
        if response.status_code == HTTPStatus.OK:
            data:Any = response.json()
            dump:str = json.dumps(data, indent=2)
            return dump
        else:
            logging.error(f"Failed to get query modules: Status {response.status_code}")
            return ""
