"""
This module provides MediaWiki data model for articles.
"""
from enum import Enum
import json
from typing import Any


class ArticleType(str, Enum):
    Empty = ""
    Main = "Main"
    User = "User"
    Template = "Template"
    Category = "Category"
    File = "File"
    Help = "Help"
    MediaWiki = "MediaWiki"
    Special = "Special"


class Article:
    """
    Represents a MediaWiki base article type.
    """

    JSON_ENCODING:str = "utf-8"
    JSON_INDENT:int = 4


    def __init__(self) -> None:
        self.type:ArticleType = ArticleType.Empty
        """The namespace for this article."""

        self.title:str = ""
        """The title of this wiki article."""

        # Composed
        # TODO: Refactor as a dictionary of sections.
        # Each section can have its own title and content.
        self.content:list[str] = []
        """The text content of this wiki article."""

        # Composed
        self.categories:list[str] = []
        """The categories of this wiki article."""


    def compose(self) -> list[str]:
        lines:list[str] = []
        lines.extend(self.content)
        lines.append("\n")
        lines.extend(self.categories)
        lines.append("\n")
        return lines


    # JSON
    #---------------------------------------------

    def data_encode(self) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "type": self.type.value,
            "title": self.title,
            "content": self.content,
            "categories": self.categories
        }
        return data


    @staticmethod
    def data_decode(data:dict[str, Any]) -> 'Article':
        """The data decoder for this class."""
        this:Article = Article()
        this.type = ArticleType(data.get("type", ArticleType.Empty.value))
        this.title = data.get("title", "")
        this.content = data.get("content", [])
        this.categories = data.get("categories", [])
        return this


    def save(self, file_path:str) -> None:
        data:dict[str, Any] = self.data_encode()
        with open(file_path, 'w', encoding=Article.JSON_ENCODING) as file:
            json.dump(data, file, indent=Article.JSON_INDENT)


    @staticmethod
    def load(file_path:str) -> 'Article':
        try:
            with open(file_path, 'r', encoding=Article.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")
        return Article.data_decode(data)
