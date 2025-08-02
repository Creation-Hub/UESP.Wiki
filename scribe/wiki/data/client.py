from scribe.wiki.data.article import Article

# TODO: This is currently unused.
class WikiClient:
    def __init__(self) -> None:
        self.articles:dict[str, Article] = {}
        """A dictionary of wiki articles indexed by their titles."""
