import logging
import os
from .article import Article

class ArticleText:

    @staticmethod
    def compose_save(article:Article, file_path:str) -> None:
        """Writes the wiki article text content to the output file."""
        lines:list[str] = article.compose()
        if not lines:
            logging.error(f"Wiki article '{file_path}' has no content to write.")
            return

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
            logging.debug(f"Created new directory for file: {os.path.dirname(file_path)}")

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


    @staticmethod
    def compose_load(file_path:str) -> list[str]:
        """Load article content from a *.wiki file."""
        if not os.path.exists(file_path):
            logging.warning(f"Wiki article file not found: '{file_path}'")
            return []
        with open(file_path, 'r', encoding='utf-8') as file:
            content:list[str] = file.readlines()
        return content
