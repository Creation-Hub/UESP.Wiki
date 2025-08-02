"""
This module provides MediaWiki data model for articles.
"""
from enum import Enum
import json
import logging
import os
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
    def __init__(self) -> None:
        self.type:ArticleType = ArticleType.Empty
        """The namespace for this article."""

        # TODO: This should be the object-key, not the file path.
        self.title:str = ""
        """The title of this wiki article."""

        self.file_path:str = ""
        """The file path of this wiki article."""

        # Composed
        self.content:list[str] = []
        """The text content of this wiki article."""

        # Composed
        self.categories:list[str] = []
        """The categories of this wiki article."""


    def _compose(self) -> list[str]:
        lines:list[str] = []
        lines.extend(self.content)
        lines.append("\n")
        lines.extend(self.categories)
        lines.append("\n")
        return lines


    def write_compose(self) -> None:
        """Writes the wiki article text content to the output file."""
        lines:list[str] = self._compose()
        if not lines:
            logging.error(f"Wiki article '{self.file_path}' has no content to write.")
            return

        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
            logging.debug(f"Created new directory for file: {os.path.dirname(self.file_path)}")

        with open(self.file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


    @staticmethod
    def load_json_data(data:dict[str, Any]) -> 'Article':
        article:Article = Article()
        article.type = ArticleType(data.get("type", ArticleType.Empty.value))
        article.title = data.get("title", "")
        article.file_path = data.get("file_path", "")
        article.content = data.get("content", [])
        article.categories = data.get("categories", [])
        return article


    @staticmethod
    def load_json(file_path:str) -> 'Article':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid wiki file format in {file_path}: {e}")
        return Article.load_json_data(data)


    @staticmethod
    def load_content(file_path:str) -> list[str]:
        """Load article content from a *.wiki file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content:list[str] = file.readlines()
        return content
