from typing import override
from sharp.collections import KeyedCollection
from .article import Article

class ArticleCollection(KeyedCollection[Article]):

    @override
    def key_for(self, item:Article) -> str:
        return item.title
