from typing import override
from sharp.collections import KeyedCollection
from scribe.publisher.article import Article, Namespace


class NamespaceCollection(KeyedCollection[Namespace]):

    def __init__(self, items:list[Namespace]|None=None) -> None:
        super().__init__(items)

    @override
    def key_for(self, item:Namespace) -> str:
        return item.name



class ArticleCollection(KeyedCollection[Article]):

    def __init__(self) -> None:
        super().__init__()

    @override
    def key_for(self, item:Article) -> str:
        return item.title.value
