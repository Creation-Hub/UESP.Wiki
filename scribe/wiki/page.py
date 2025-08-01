from scribe.wiki.article import Article

class Page(Article):
    """
    Represents a MediaWiki page type.
    """
    def __init__(self) -> None:
        super().__init__()
