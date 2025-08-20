from typing import override
from sharp.collections import KeyedCollection
from wiki.data.namespaces import Namespace
from wiki.data.title import Title
from .article import Article

class NamespaceCollection(KeyedCollection[str, Namespace]):

    def __init__(self, items:list[Namespace]|None=None) -> None:
        super().__init__(items)

    @override
    def key_for(self, item:Namespace) -> str:
        return item.name



class ArticleCollection(KeyedCollection[Title, Article]):

    def __init__(self) -> None:
        super().__init__()

    @override
    def key_for(self, item:Article) -> Title:
        return item.title
