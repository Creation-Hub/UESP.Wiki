import os
from typing import Any, override
from sharp.collections import KeyedCollection
from wiki.data.common import Namespaces
from wiki.data.namespaces import Namespace
from wiki.data.title import Title
from .article import Article
from .article_text import ArticleText, ArticlePath

class ArticleCollection(KeyedCollection[Title, Article]):

    def __init__(self) -> None:
        super().__init__()


    @override
    def key_for(self, item:Article) -> Title:
        return item.title


    def encode(self, file_path:str) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {}
        data["articles"] = {}
        for key, item in self.items():
            page_file_path:str = ArticlePath.get_filepath(item, os.path.dirname(file_path), "").replace(":", "\\")
            ArticleText.compose_save(item, page_file_path)
            data["articles"][key.value] = ArticleJson.encode(item, page_file_path)
        return data


    @staticmethod
    def decode(data:dict[str, Any]) -> 'ArticleCollection':
        """The data decoder for this class."""
        articles:dict[str, Any] = data.get("articles", {})

        collection:ArticleCollection = ArticleCollection()
        for article_data in articles.values():
            article_data:dict[str, Any] = article_data
            article:Article = ArticleJson.decode(article_data)
            collection.add(article)
        return collection


class ArticleJson:

    @staticmethod
    def encode(this:Article, file_path:str) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "name": this.title.name
        }

        if this.title.namespace:
            data["namespace"] = this.title.namespace.name

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
