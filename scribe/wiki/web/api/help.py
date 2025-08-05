"""
https://www.mediawiki.org/w/api.php?action=help
"""
import logging
import requests
from http import HTTPStatus
from requests import Response
from scribe.wiki.web.api.actions import Action
from scribe.wiki.web.api.main import Main
from scribe.wiki.web.site import Site


class Help:

    @staticmethod
    def help(site:Site) -> str:
        """Get general API help and available modules"""
        parameters:dict[str, str] = {
            Main.ACTION: Action.HELP
        }
        response:Response = requests.get(site.api_url, params=parameters)
        if response.status_code == HTTPStatus.OK:
            return response.text
        else:
            logging.error(f"Failed to get API help: Status {response.status_code}")
            return ""
