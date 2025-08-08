from typing import override
from scribe.shared.collections import KeyedCollectionAbstract
from .article import Article

class ArticleCollection(KeyedCollectionAbstract[Article]):

    @override
    def key_for(self, item:Article) -> str:
        return item.title
