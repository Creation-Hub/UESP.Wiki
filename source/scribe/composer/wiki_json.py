import json
from typing import Any
from wiki.data.namespaces import Namespace
from wiki.data.common import Namespaces
from wiki.data.title import Title
from .article import Article
from .article_text import ArticleText
from .wiki import Wiki


class WikiJson:

    JSON_ENCODING:str = "utf-8"
    """The default JSON encoding to use."""

    JSON_INDENT:int = 4
    """The default JSON indentation to use."""


    @staticmethod
    def save(this:Wiki, file_path:str) -> None:
        data:dict[str, Any] = WikiJson.encode(this, file_path)
        with open(file_path, 'w', encoding=WikiJson.JSON_ENCODING) as file:
            json.dump(data, file, indent=WikiJson.JSON_INDENT)


    @staticmethod
    def load(file_path:str) -> Wiki:
        try:
            with open(file_path, 'r', encoding=WikiJson.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")
        return WikiJson.decode(data)


    # Data
    #---------------------------------------------

    @staticmethod
    def encode(this:Wiki, file_path:str) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {}
        data["articles"] = {}
        for key, article in this.articles.items():
            data["articles"][key.value] = ArticleJson.encode(article, file_path)
        return data


    @staticmethod
    def decode(data:dict[str, Any]) -> Wiki:
        """The data decoder for this class."""
        articles:dict[str, Any] = data.get("articles", {})
        this:Wiki = Wiki()
        for article_data in articles.values():
            article_data:dict[str, Any] = article_data
            article:Article = ArticleJson.decode(article_data)
            this.articles.add(article)
        return this


class ArticleJson:

    @staticmethod
    def encode(this:Article, file_path:str) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "name": this.title.name
        }

        if this.title.namespace:
            data["namespace"] = this.title.namespace.name

        # TODO: WIP: Limit content size for JSON.
        #       Possibly store filepath to content instead.
        if this.content:
            data["content"] = file_path

        # TODO: WIP
        if this.categories:
            data["categories"] = [category.name for category in this.categories]
        return data


    @staticmethod
    def decode(data:dict[str, Any]) -> Article:
        """The data decoder for this class."""
        # Decode the title
        this_name:str = ArticleJson._name(data.get("name"))
        this_namespace:Namespace = Namespace(data.get("namespace", ""))
        title:Title = Title(this_name, this_namespace)

        # Decode the article
        article:Article = Article(title)
        file_path:str = data.get("content", "")
        article.content = ArticleText.compose_load(file_path)
        article.categories = [Title(category_name, Namespaces.Category) for category_name in data.get("categories", [])]
        return article


    @staticmethod
    def _name(name:str|None) -> str:
        if name is None or name == "":
            raise ValueError(f"Article must have a valid name. name={name}")
        return name
