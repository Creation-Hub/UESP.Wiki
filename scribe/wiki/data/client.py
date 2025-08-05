import json
from typing import Any
from scribe.wiki.data.article import Article

class DataClient:
    JSON_ENCODING:str = "utf-8"
    JSON_INDENT:int = 4


    def __init__(self) -> None:
        self.articles:dict[str, Article] = {}
        """A dictionary of wiki articles indexed by their titles."""


    # Articles
    #---------------------------------------------

    def get(self, key:str) -> Article:
        return self.articles[key]


    def add(self, article:Article) -> None:
        """Adds an article to the wiki context."""
        if not article.title:
            raise ValueError("Article title cannot be empty.")
        self.articles[article.title] = article


    # JSON
    #---------------------------------------------

    def data_encode(self) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {}
        data["articles"] = {}
        for key, article in self.articles.items():
            data["articles"][key] = article.data_encode()
        return data


    @staticmethod
    def data_decode(data:dict[str, Any]) -> 'DataClient':
        """The data decoder for this class."""
        articles:dict[str, Any] = data.get("articles", {})
        this:DataClient = DataClient()
        for article_data in articles.values():
            article_data:dict[str, Any] = article_data
            article:Article = Article.data_decode(article_data)
            this.add(article)
        return this


    def save(self, file_path:str) -> None:
        data:dict[str, Any] = self.data_encode()
        with open(file_path, 'w', encoding=DataClient.JSON_ENCODING) as file:
            json.dump(data, file, indent=DataClient.JSON_INDENT)


    @staticmethod
    def load(file_path:str) -> 'DataClient':
        try:
            with open(file_path, 'r', encoding=DataClient.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")
        return DataClient.data_decode(data)
