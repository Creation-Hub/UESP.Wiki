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

        directory:str = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.debug(f"Created new directory for file: {directory}")

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


class ArticlePath:

    @staticmethod
    def get_filepath(article:Article, base_directory:str, project:str) -> str:
        """Generate complete file path for an article."""
        namespace_dir:str = ""
        if article.title.namespace.name:
            namespace_dir = article.title.namespace.name
        else:
            namespace_dir = "Main"

        filename:str = article.title.name + ".wiki"
        return os.path.join(base_directory, namespace_dir, project, filename)
