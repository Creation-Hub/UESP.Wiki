"""
Provides a site configuration for the MediaWiki API client.
"""
import json
from typing import Any


class Site:
    INDEX_PATH:str = "/index.php"
    API_PATH:str = "/api.php"
    REST_PATH:str = "/rest.php"


    def __init__(self, url:str) -> None:
        super().__init__()
        self.url:str = url
        self.article_path:str|None = None
        self.script_path:str|None = None
        self.index_path:str = Site.INDEX_PATH
        self.api_path:str = Site.API_PATH
        self.rest_path:str = Site.REST_PATH

    @property
    def article_url(self) -> str:
        if self.article_path:
            return self.url + self.article_path
        else:
            return self.url + self.index_path

    @property
    def api_url(self) -> str:
        if self.script_path:
            return self.url + self.script_path + self.api_path
        else:
            return self.url + self.api_path

    @property
    def rest_url(self) -> str:
        if self.script_path:
            return self.url + self.script_path + self.rest_path
        else:
            return self.url + self.rest_path


def create_site(path:str, environment_id:str) -> Site:
    with open(path, "r") as file:
        data:dict[str, Any] = json.load(file)

    environments:dict[str, Any] = data.get("environments", [])
    environment:dict[str, str] = environments.get(environment_id, {})

    url:str = environment.get("url", "")
    site:Site = Site(url)
    site.article_path = environment.get("article", site.article_path)
    site.script_path = environment.get("script", site.script_path)
    site.api_path = environment.get("api", site.api_path)
    site.rest_path = environment.get("rest", site.rest_path)
    site.index_path = environment.get("index", site.index_path)
    return site
