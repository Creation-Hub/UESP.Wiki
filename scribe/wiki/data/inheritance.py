"""
Provides methods to format inheritance data for scripts.
"""
from collections.abc import Iterable
from scribe.papyrus.code import Script
from scribe.wiki.formatter import WikiFormatter

class WikiDataInheritance:
    """
    Provides formatting and retrieving inheritance information for scripts.
    """

    # Inheritance Chain
    #---------------------------------------------

    @staticmethod
    def _to_names_linked(scripts:list[Script]) -> list[str]:
        return [WikiFormatter.link_script_object(str(script.header.name)) for script in scripts] if scripts else []


    @staticmethod
    def format_inheritance_chain(inheritance_chain:list[Script]) -> str:
        """
        Gets the inheritance chain as a string for the 'extends' field in script templates.
        """
        if not inheritance_chain:
            return "Nothing"
        else:
            names:list[str] = WikiDataInheritance._to_names_linked(inheritance_chain)
            return " → ".join(names)


    # Inheritance
    #---------------------------------------------

    @staticmethod
    def _to_names(scripts:list[Script]) -> list[str]:
        return [str(script.header.name) for script in scripts] if scripts else []


    @staticmethod
    def get_inheritance_string(script:Script, inheritance_chain:list[Script]) -> str:
        """
        Gets the inheritance chain as a string for the script index page.
        """
        chain_reversed:Iterable[Script] = reversed(inheritance_chain)
        inheritance_list:list[Script] = list(chain_reversed) + [script]
        names:list[str] = WikiDataInheritance._to_names(inheritance_list)
        return " ← ".join(names)
