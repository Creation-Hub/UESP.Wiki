"""
This module provides MediaWiki data model for articles.

- https://www.mediawiki.org/wiki/Manual:Page_table
- https://www.mediawiki.org/wiki/Help:Categories
"""
from typing import override
from wiki.data.title import Title

class Article:
    """
    Represents a MediaWiki base article type.
    """

    def __init__(self, title:Title) -> None:
        super().__init__()

        self.title:Title = title
        """The full title path of this article."""

        self.content:list[str] = []
        """The text content of this wiki article."""

        self.categories:list[Title] = []
        """The categories this wiki article belongs to."""

        self.templates:list[Title] = []
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
        for title in self.categories:
            lines.append(title.link)
            lines.append("\n")
        return lines
