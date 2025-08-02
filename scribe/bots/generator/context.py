"""
Used to configure the wiki context.
"""
from datetime import datetime
import json
import os
from typing import Any
from scribe.wiki.data.article import Article, ArticleType
from scribe.wiki.data.page import Page

class GeneratorContext:
    """
    Provides features for the wiki context.
    """

    FILENAME:str = "wiki.json"
    """The filename for the wiki manifest file."""


    def __init__(self) -> None:

        # TODO: Refactor this as a dictionary type that belongs to the wiki.data module.
        self.articles:dict[str, Article] = {}
        """A dictionary of wiki articles indexed by their titles."""

        self.version:str = ""
        self.generated_time:str = ""
        self.generator_version:str = ""


    @staticmethod
    def create() -> 'GeneratorContext':
        this:GeneratorContext = GeneratorContext()
        this.generated_time = datetime.now().isoformat()
        this.generator_version = "1.0.0"  # Get from app version

        # This is a dummy for page data.
        user_page:Page = Page()
        user_page.type = ArticleType.User
        user_page.title = "User:Scrivener07"
        user_page.file_path = "User-Scrivener07.wiki"
        user_page.content = ["My name is Scrivener and I have been modding since TES4 Oblivion."]
        user_page.categories = []
        this.add(user_page)

        # This is a dummy for page data.
        bot_page:Page = Page()
        bot_page.type = ArticleType.User
        bot_page.title = "User:Scrivener07/Bot"
        bot_page.file_path = "User-Scrivener07-Bot.wiki"
        bot_page.content = ["This is the Scribe Bot wiki page."]
        user_page.categories = []
        this.add(bot_page)

        return this


    # Articles
    #---------------------------------------------

    def add(self, article:Article) -> None:
        """Adds an article to the wiki context."""

        if not article.title:
            raise ValueError("Article title cannot be empty.")

        self.articles[article.title] = article


    def get(self, key:str) -> Article:
        return self.articles[key]


    # Serialize
    #---------------------------------------------

    def save_data(self) -> dict[str, Any]:
        data:dict[str, Any] = {
            "version": self.version,
            "generated_at": self.generated_time,
            "generator_version": self.generator_version,
            "articles": {}
        }
        data_articles:dict[str, Any] = data["articles"]
        for key, article in self.articles.items():
            article:Article = article
            data_articles[key] = {
                "file_path": article.file_path,
                "namespace": article.type.value,
                "title": article.title,
                "content": article.content,
                "categories": article.categories
            }
        return data


    def save(self, export_directory:str) -> str:
        data:dict[str, Any] = self.save_data()
        file_path:str = os.path.join(export_directory, GeneratorContext.FILENAME)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return file_path


    # Deserialize
    #---------------------------------------------

    @staticmethod
    def load_data(data:dict[str, Any]) -> 'GeneratorContext':
        this:GeneratorContext = GeneratorContext()
        this.version = data.get("version", "1.0")
        this.generated_time = data.get("generated_at", "")
        this.generator_version = data.get("generator_version", "")
        articles:dict[str, Any] = data.get("articles", {})
        for article_data in articles.values():
            article_data:dict[str, Any] = article_data
            article:Article = Article.load_json_data(article_data)
            this.add(article)
        return this


    @staticmethod
    def load(file_path:str) -> 'GeneratorContext':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid wiki file format in {file_path}: {e}")
        this:GeneratorContext = GeneratorContext.load_data(data)
        return this
