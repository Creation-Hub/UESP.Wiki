"""
Provides methods formatting for MediaWiki content.

- https://www.mediawiki.org/wiki/Help:Formatting
- https://www.mediawiki.org/wiki/Help:Lists
- https://www.mediawiki.org/wiki/Help:Tables
- https://www.mediawiki.org/wiki/Help:Links
"""
from wiki.data.section import SectionLevel

class Text:
    """
    Provides methods formatting for MediaWiki content.
    """


    @staticmethod
    def italic(text:str) -> str:
        return f"''{text}''"


    @staticmethod
    def bold(text:str) -> str:
        return f"'''{text}'''"


    @staticmethod
    def bold_italic(text:str) -> str:
        return f"'''''{text}'''''"


    @staticmethod
    def escape(text:str) -> str:
        return f"<nowiki>{text}</nowiki>"


    @staticmethod
    def section(name:str, level:SectionLevel) -> str:
        decorator:str = "=" * level
        return f"{decorator} {name} {decorator}"


    @staticmethod
    def rule() -> str:
        return f"----"


    @staticmethod
    def indent(text:str, level:int) -> str:
        decorator:str = ":" * level
        return f"{decorator} {text}"


    @staticmethod
    def list_csv(items:list[str]) -> str:
        """Convert a list of items into a comma-separated string."""
        return ", ".join(items) if items else ""


    @staticmethod
    def list_bullet(items:list[str]) -> str:
        return "\n* ".join(items) if items else ""


    @staticmethod
    def list_number(items:list[str]) -> str:
        return "\n# ".join(items) if items else ""


    @staticmethod
    def list_definition(items:dict[str, list[str]]) -> str:
        text:str = ""
        for item in items:
            text += f"\n;{item}"
            definitions:list[str] = items[item]
            for definition in definitions:
                text += f"\n:{definition}"
        return text
