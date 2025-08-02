"""
Provides wiki template generation features.
"""
from scribe.wiki.data.article import Article

class Template(Article):
    """
    Represents a MediaWiki template type.
    """
    def __init__(self) -> None:
        super().__init__()
        # TODO: Add a "help" page reference for templates.


    @staticmethod
    def create(file_path:str) -> 'Template':
        this:Template = Template()
        this.file_path = file_path
        return this
