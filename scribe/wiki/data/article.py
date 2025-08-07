"""
This module provides MediaWiki data model for articles.
"""
import json
from typing import Any


class Namespace:
    """
    Represents the built-in MediaWiki namespaces.
    """
    Empty:str = ""
    Main:str = "Main"
    User:str = "User"
    Template:str = "Template"
    Category:str = "Category"
    File:str = "File"
    Help:str = "Help"
    MediaWiki:str = "MediaWiki"
    Special:str = "Special"


class Article:
    """
    Represents a MediaWiki base article type.
    """

    JSON_ENCODING:str = "utf-8"
    JSON_INDENT:int = 4


    def __init__(self) -> None:
        super().__init__()

        self.name:str = ""
        """The name of this wiki article. Excludes the namespace."""

        self.namespace:str = Namespace.Empty
        """The namespace for this article."""

        # Composed
        # TODO: Refactor as a dictionary of sections [str, str].
        # Each section can have its own title and content.
        self.content:list[str] = []
        """The text content of this wiki article."""

        # Composed
        self.categories:list[Category] = []
        """The categories of this wiki article."""

        self.templates:list[Template] = []


    @property
    def title(self) -> str:
        if self.namespace == Namespace.Empty:
            return f"{self.name}"
        else:
            return f"{self.namespace}:{self.name}"

    @property
    def link(self) -> str:
        return f"[[{self.title}]]"



    def compose(self) -> list[str]:
        """Compose the complete wiki markup."""
        lines:list[str] = self.content.copy()
        lines.append("\n")
        for category in self.categories:
            lines.append(category.link)
            lines.append("\n")
        return lines


    # JSON
    #---------------------------------------------

    def data_encode(self) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "name": self.name,
            "namespace": self.namespace,
            "content": self.content[:5], # Limit content size for JSON (TODO: WIP)
            "categories": [category.name for category in self.categories] # TODO: WIP
        }
        return data


    @staticmethod
    def data_decode(data:dict[str, Any]) -> 'Article':
        """The data decoder for this class."""
        this:Article = Article()
        this.namespace = data.get("namespace", "")
        this.name = data.get("name", "")
        this.content = data.get("content", [])
        # Convert string categories back to Category objects
        category_names:list[Any] = data.get("categories", [])
        for name in category_names:
            if isinstance(name, str):
                category:Category = Category()
                category.name = name
                this.categories.append(category)
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



class Page(Article):
    """
    Represents a MediaWiki page type.
    """
    def __init__(self) -> None:
        super().__init__()
        self.namespace = Namespace.Empty

    @staticmethod
    def create(file_path:str) -> Article:
        raise NotImplementedError("Page creation is not implemented yet.")


class Category(Article):
    """
    Represents a MediaWiki category type.
    """
    def __init__(self) -> None:
        super().__init__()
        self.namespace = Namespace.Category

    @staticmethod
    def create(file_path:str) -> 'Category':
        raise NotImplementedError("Category creation is not implemented yet.")


class Template(Article):
    """
    Represents a MediaWiki template type.
    """
    def __init__(self) -> None:
        super().__init__()
        self.namespace = Namespace.Template

    @staticmethod
    def create(file_path:str) -> 'Template':
        raise NotImplementedError("Template creation is not implemented yet.")
