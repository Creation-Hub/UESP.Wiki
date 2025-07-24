import json

class Site:
    def __init__(self, url:str) -> None:
        self.URL:str = url
        self.URL_ARTICLE:str = ""
        self.URL_SCRIPT:str = ""
        self.URL_INDEX:str = "/index.php"
        self.URL_API:str = "/api.php"
        self.URL_REST:str = "/rest.php"

    @property
    def API(self) -> str:
        if self.URL_SCRIPT:
            return self.URL + self.URL_SCRIPT + self.URL_API
        else:
            return self.URL + self.URL_API

    @property
    def REST(self) -> str:
        if self.URL_SCRIPT:
            return self.URL + self.URL_SCRIPT + self.URL_REST
        else:
            return self.URL + self.URL_REST

    @property
    def Article(self) -> str:
        return self.URL + self.URL_ARTICLE


def create_site(path:str, environment:str) -> Site:
    with open(path, "r") as file:
        settings = json.load(file)

    configuration:dict[str, str] = settings[environment]
    url:str = configuration["url"]

    site:Site = Site(url)
    site.URL_SCRIPT = configuration.get("script", site.URL_SCRIPT)
    site.URL_API = configuration.get("api", site.URL_API)
    site.URL_REST = configuration.get("rest", site.URL_REST)
    site.URL_INDEX = configuration.get("index", site.URL_INDEX)
    site.URL_ARTICLE = configuration.get("article", site.URL_ARTICLE)
    return site
