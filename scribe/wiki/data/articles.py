from typing import override
from scribe.shared.collections import KeyedCollection
from .article import Article

class ArticleCollection(KeyedCollection[Article]):

    @override
    def key_for(self, item:Article) -> str:
        return item.title
