from http import HTTPStatus
import json
from typing import Any
import requests
from requests import Response
from uesp.web.clients.site import Site


def help(site:Site) -> str:
    """Get general API help and available modules"""
    parameters:dict[str, str] = {
        "action": "help"
    }
    response:Response = requests.get(site.API, params=parameters)
    if response.status_code == HTTPStatus.OK:
        return response.text
    else:
        print(f"Failed to get API help: Status {response.status_code}")
        return ""


def info(site:Site) -> str:
    """Get basic wiki information"""
    parameters:dict[str, str] = {
        "action": "query",
        "meta": "siteinfo",
        "format": "json"
    }
    response:Response = requests.get(site.API, params=parameters)
    if response.status_code == HTTPStatus.OK:
        data:Any = response.json()
        dump:str = json.dumps(data, indent=2)
        return dump
    else:
        print(f"Failed to get site info: Status {response.status_code}")
        return ""


def modules(site:Site) -> str:
    """Get list of available API modules"""
    parameters:dict[str, str] = {
        "action": "paraminfo",
        "format": "json"
    }
    response:Response = requests.get(site.API, params=parameters)
    if response.status_code == HTTPStatus.OK:
        data:Any = response.json()
        dump:str = json.dumps(data, indent=2)
        return dump
    else:
        print(f"Failed to get query modules: Status {response.status_code}")
        return ""


def modules_query(site:Site) -> str:
    """Get available query modules (what you can query for)"""
    parameters:dict[str, str] = {
        "action": "paraminfo",
        "modules": "query",
        "format": "json"
    }
    response:Response = requests.get(site.API, params=parameters)
    if response.status_code == HTTPStatus.OK:
        data:Any = response.json()
        dump:str = json.dumps(data, indent=2)
        return dump
    else:
        print(f"Failed to get query modules: Status {response.status_code}")
        return ""
