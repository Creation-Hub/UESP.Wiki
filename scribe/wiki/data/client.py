"""
The wiki data client provides object relationship management.
"""
import json
from typing import Any
from .article import Article
from .article import Page, Category, Template
from .articles import ArticleCollection

class ArticleClient:

    JSON_ENCODING:str = "utf-8"
    """The default JSON encoding to use."""

    JSON_INDENT:int = 4
    """The default JSON indentation to use."""

    JSON_FILENAME:str = "wiki.json"
    """The default JSON file name to use."""


    def __init__(self) -> None:
        super().__init__()
        self.articles:ArticleCollection = ArticleCollection()
        """A dictionary of wiki articles indexed by their titles."""
        self.templates:dict[str, Template] = {}
        self.categories:dict[str, Category] = {}
        self.pages:dict[str, Page] = {}


    # Articles
    #---------------------------------------------

    def get_article(self, key:str) -> Article:
        return self.articles[key]


    # Typed
    #---------------------------------------------

    def add(self, article:Article) -> None:
        """Add article and maintain typed collections."""
        if not article.title:
            raise ValueError("Article title cannot be empty.")

        # Add the article.
        self.articles.add(article)

        # Maintain typed collections
        if isinstance(article, Category):
            self.categories[article.title] = article
        elif isinstance(article, Template):
            self.templates[article.title] = article
        elif isinstance(article, Page):
            self.pages[article.title] = article


    #---------------------------------------------


    def get_or_create_category(self, name:str) -> Category:
        """Get existing category or create new one."""
        if name in self.categories:
            return self.categories[name]

        category:Category = Category()
        category.name = name
        self.add(category)
        return category


    def get_or_create_template(self, name:str) -> Template:
        """Get existing template or create new one."""
        if name in self.templates:
            return self.templates[name]

        template:Template = Template()
        template.name = name
        self.add(template)
        return template


    #---------------------------------------------


    def link_page_to_category(self, page_title:str, category_name:str) -> None:
        """Create relationship between page and category."""
        if page_title not in self.articles:
            raise ValueError(f"Page not found: {page_title}")

        page:Article = self.articles[page_title]
        category = self.get_or_create_category(category_name)
        ArticleClient.add_category(page, category)


    #---------------------------------------------


    @staticmethod
    def add_category(this:Article, category:Category) -> None:
        """Add a category reference."""
        if category not in this.categories:
            this.categories.append(category)

    @staticmethod
    def add_template(this:Article, template:Template) -> None:
        """Add a template reference."""
        if template not in this.templates:
            this.templates.append(template)


    # JSON
    #---------------------------------------------

    def data_encode(self) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {}
        data["articles"] = {}
        for key, article in self.articles.items():
            data["articles"][key] = article.data_encode()
        return data


    @staticmethod
    def data_decode(data:dict[str, Any]) -> 'ArticleClient':
        """The data decoder for this class."""
        articles:dict[str, Any] = data.get("articles", {})
        this:ArticleClient = ArticleClient()
        for article_data in articles.values():
            article_data:dict[str, Any] = article_data
            article:Article = Article.data_decode(article_data)
            this.add(article)
        return this


    def save(self, file_path:str) -> None:
        data:dict[str, Any] = self.data_encode()
        with open(file_path, 'w', encoding=ArticleClient.JSON_ENCODING) as file:
            json.dump(data, file, indent=ArticleClient.JSON_INDENT)


    @staticmethod
    def load(file_path:str) -> 'ArticleClient':
        try:
            with open(file_path, 'r', encoding=ArticleClient.JSON_ENCODING) as file:
                data:dict[str, Any] = json.load(file)
        except json.JSONDecodeError as jsonDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}: {jsonDecodeError}")
        return ArticleClient.data_decode(data)
