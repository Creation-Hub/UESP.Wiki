"""
Used to configure the wiki context.
"""
from scribe.wiki.category import Category
from scribe.wiki.page import Page
from scribe.wiki.template import Template

class WikiContext:
    """
    Provides features for the wiki context.
    """
    def __init__(self) -> None:
        self.pages:list[Page] = []
        """The list of wiki pages to use."""

        self.categories:list[Category] = []
        """The list of wiki categories to use."""

        self.templates:list[Template] = []
        """The list of wiki templates to use."""


    @staticmethod
    def create() -> 'WikiContext':
        this:WikiContext = WikiContext()
        return this
