"""
Provides object relationship management for wiki data.
"""
import logging
import os
import json
from typing import Any
from scribe.app.log import Log
from scribe.app.context import AppConfiguration
from scribe.composer.wiki_collection import ArticleCollection

class ComposerService:
    NAME:str = "Composer"
    """The name of this service."""


    def __init__(self) -> None:
        super().__init__()

        self.export_directory:str = ""
        """The export directory for wiki pages."""

        self.articles:ArticleCollection = ArticleCollection()
        """A dictionary of wiki articles indexed by their titles."""


    @staticmethod
    def create(configuration:AppConfiguration) -> 'ComposerService':
        if not configuration.export_directory:
            raise ValueError("No `export_directory` specified in app configuration.")

        logging.info(f" {ComposerService.NAME} ".center(Log.DIV_WIDTH, "-"))
        this:ComposerService = ComposerService()
        this.export_directory = configuration.export_directory
        return this


    # JSON
    #---------------------------------------------

    JSON_FILENAME:str = "wiki.json"
    """The default JSON file name to use."""

    JSON_ENCODING:str = "utf-8"
    """The default JSON encoding to use."""

    JSON_INDENT:int = 4
    """The default JSON indentation to use."""


    def save(self) -> None:
        file_path:str = os.path.join(self.export_directory, ComposerService.JSON_FILENAME)
        data:dict[str, Any] = self.articles.encode(file_path)
        with open(file_path, 'w', encoding=ComposerService.JSON_ENCODING) as file:
            json.dump(data, file, indent=ComposerService.JSON_INDENT)
        logging.info(f"Saved {len(self.articles)} articles to '{file_path}'.")


    def load(self) -> None:
        file_path:str = os.path.join(self.export_directory, ComposerService.JSON_FILENAME)
        try:
            with open(file_path, 'r', encoding=ComposerService.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")

        self.articles = ArticleCollection.decode(data)
        logging.info(f"Loaded {len(self.articles)} articles from '{file_path}'.")
