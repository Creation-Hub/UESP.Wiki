"""
This module provides MediaWiki data model for articles.
"""
"""
- https://www.mediawiki.org/wiki/Manual:Page_table
- https://www.mediawiki.org/wiki/Manual:Page_ID
- https://www.mediawiki.org/wiki/Manual:Page_title
- https://www.mediawiki.org/wiki/Manual:Title.php

A page whose name is not prefixed by a namespace lies in the mainspace.

Note, however, that colons and prefixes can also appear in page titles without indicating a namespace:
    the page `Foo:Namespaces` is a page located in the mainspace because the namespace 'Foo' does not exist.

Similarly the page `Help:Foo:Namespaces` is in the 'Help' namespace.

prefix:	namespace:	page name
optional	optional	required
"""
"""
- https://www.mediawiki.org/wiki/Help:Categories
"""
from typing import override
from wiki.data.namespaces import Namespace
from wiki.data.title import Title

class Article:
    """
    Represents a MediaWiki base article type.
    """

    def __init__(self, name:str, namespace:Namespace) -> None:
        super().__init__()

        self.title:Title = Title(name, namespace)
        """The full title path of this article."""

        # Composed
        self.content:list[str] = []
        """The text content of this wiki article."""

        self.categories:list[Article] = []
        """The categories this wiki article belongs to."""

        self.templates:list[Article] = []
        """The templates used by this wiki article."""


    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r}, content={self.content!r}, categories={self.categories!r}, templates={self.templates!r})"


    @override
    def __str__(self) -> str:
        return str(self.title)


    def compose(self) -> list[str]:
        """Compose the complete wiki markup."""
        lines:list[str] = self.content.copy()
        lines.append("\n")
        for category in self.categories:
            lines.append(category.title.link)
            lines.append("\n")
        return lines
