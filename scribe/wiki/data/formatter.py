"""
Provides methods formatting for MediaWiki content.
"""

class WikiFormatter:
    """
    Provides methods formatting for MediaWiki content.
    """

    @staticmethod
    def to_list_csv(items:list[str]) -> str:
        """Convert a list of items into a comma-separated string."""
        return ", ".join(items) if items else ""
