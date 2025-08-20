import logging
import os
from scribe.app.context import AppConfiguration
from scribe.composer.wiki import Wiki
from scribe.composer.wiki_json import WikiJson

class ComposerService:

    JSON_FILENAME:str = "wiki.json"
    """The default JSON file name to use."""


    def __init__(self) -> None:
        super().__init__()
        self.export_directory:str = ""
        self.wiki:Wiki = Wiki()


    @staticmethod
    def create(configuration:AppConfiguration) -> 'ComposerService':
        if not configuration.export_directory:
            raise ValueError("No `export_directory` specified in app configuration.")

        this:ComposerService = ComposerService()
        this.wiki = Wiki.create()
        this.export_directory = configuration.export_directory
        return this


    def load(self) -> None:
        wiki_file_path:str = os.path.join(self.export_directory, ComposerService.JSON_FILENAME)
        self.wiki = WikiJson.load(wiki_file_path)
        logging.info(f"Loaded {len(self.wiki.articles)} articles from '{wiki_file_path}'.")


    def save(self) -> None:
        wiki_file_path:str = os.path.join(self.export_directory, ComposerService.JSON_FILENAME)
        WikiJson.save(self.wiki, wiki_file_path)
        logging.info(f"Saved {len(self.wiki.articles)} articles to '{wiki_file_path}'.")
