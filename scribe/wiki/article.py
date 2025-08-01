"""
Help:
    - https://www.mediawiki.org/wiki/Manual:Page_content_models
    - https://www.mediawiki.org/wiki/Help:Namespaces
"""

import logging
import os

class Article:
    """
    Represents a MediaWiki base article type.
    """
    def __init__(self) -> None:
        self.file_path:str = ""
        """The file path of this wiki page."""

        self.title:str = ""
        """The title of this wiki page."""

        self.content:list[str] = []
        """The text content of this wiki page."""

        self.categories:list[str] = []
        """The categories of this wiki page."""


    def compose(self) -> list[str]:
        lines:list[str] = []
        lines.extend(self.content)
        lines.extend(self.categories)
        return lines


    def write(self) -> None:
        """Writes the wiki page text content to the output file."""
        lines:list[str] = self.compose()
        if not lines:
            logging.error(f"Wiki page '{self.file_path}' has no content to write.")
            return

        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
            logging.debug(f"Created new directory for file: {os.path.dirname(self.file_path)}")

        with open(self.file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
