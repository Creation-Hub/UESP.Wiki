import json
from typing import Any
from wiki.data.namespaces import Namespace
from wiki.data.title import Title
from scribe.publisher.article import Article
from scribe.publisher.wiki import Wiki


class WikiJson:

    JSON_ENCODING:str = "utf-8"
    """The default JSON encoding to use."""

    JSON_INDENT:int = 4
    """The default JSON indentation to use."""

    JSON_FILENAME:str = "wiki.json"
    """The default JSON file name to use."""


    @staticmethod
    def save(this:Wiki, file_path:str) -> None:
        data:dict[str, Any] = WikiJson.encode(this)
        with open(file_path, 'w', encoding=WikiJson.JSON_ENCODING) as file:
            json.dump(data, file, indent=WikiJson.JSON_INDENT)


    @staticmethod
    def load(wiki:Wiki, file_path:str) -> Wiki:
        try:
            with open(file_path, 'r', encoding=WikiJson.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")
        return WikiJson.decode(wiki, data)


    # Data
    #---------------------------------------------

    @staticmethod
    def encode(this:Wiki) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {}
        # data["namespaces"] = this.namespaces.keys()
        data["articles"] = {}
        for key, article in this.articles.items():
            data["articles"][key.name] = ArticleJson.encode(article)
        return data


    @staticmethod
    def decode(wiki:Wiki, data:dict[str, Any]) -> Wiki:
        """The data decoder for this class."""
        articles:dict[str, Any] = data.get("articles", {})
        # this:Wiki = Wiki()
        for article_data in articles.values():
            article_data:dict[str, Any] = article_data
            article:Article = ArticleJson.decode(wiki, article_data)
            wiki.articles.add(article)
        return wiki


class ArticleJson:

    JSON_ENCODING:str = "utf-8"
    JSON_INDENT:int = 4


    @staticmethod
    def _save(this:Article, file_path:str) -> None:
        data:dict[str, Any] = ArticleJson.encode(this)
        with open(file_path, 'w', encoding=ArticleJson.JSON_ENCODING) as file:
            json.dump(data, file, indent=ArticleJson.JSON_INDENT)


    @staticmethod
    def _load(wiki:Wiki, file_path:str) -> Article:
        try:
            with open(file_path, 'r', encoding=ArticleJson.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")
        return ArticleJson.decode(wiki, data)


    # Data
    #---------------------------------------------

    @staticmethod
    def encode(this:Article) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "name": this.title.name
        }

        if this.title.namespace:
            data["namespace"] = this.title.namespace.name

        # TODO: WIP: Limit content size for JSON.
        #       Possibly store filepath to content instead.
        if this.content:
            data["content"] = this.content[:5]

        # TODO: WIP
        if this.categories:
            data["categories"] = [category.name for category in this.categories]
        return data


    @staticmethod
    def decode(wiki:Wiki, data:dict[str, Any]) -> Article:
        """The data decoder for this class."""
        this_name:str = ArticleJson._name(data.get("name"))
        this_namespace:Namespace = ArticleJson._namespace(wiki, data.get("namespace"))
        this:Title = Title(this_name, this_namespace)
        # this.content = data.get("content", [])
        # # Convert string categories back to Category objects
        # category_names:list[Any] = data.get("categories", [])
        # for name in category_names:
        #     if isinstance(name, str):
        #         category:Title = Title(name, Namespaces.Category)
        #         this.categories.append(category)
        return Article(this)


    @staticmethod
    def _name(name:str|None) -> str:
        if name is None or name == "":
            raise ValueError("Article must have a valid name.")
        return name


    @staticmethod
    def _namespace(wiki:Wiki, namespace_name:str|None) -> Namespace:
        if namespace_name is None:
            raise ValueError("Article must have a valid namespace name.")

        namespace:Namespace|None = wiki.namespaces.get(namespace_name)
        if namespace is None:
            raise ValueError("Article must match a defined namespace.")
        return namespace
