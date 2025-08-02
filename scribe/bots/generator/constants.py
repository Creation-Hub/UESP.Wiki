class Wiki:
    """
    Constants for the UESP Wiki.
    This class contains constants that are used throughout the wiki generation process.
    These fields should be considered TODO for implementating with configurable options.
    """

    CATEGORY_TEMPLATES_INFOBOX:str = "Category:Infobox_Templates"
    """
    The category for article-templates that provide information boxes.
    This string is used in the template definition directly and does not have internal link syntax.
    """

    CATEGORY_PAPYRUS:str = "[[Category:Starfield_Mod-Papyrus]]"
    """
    The category for Papyrus scripts and related articles.
    This is used within page content to categorize articles related to Papyrus scripts.
    This DOES have internal link syntax.
    """


    @staticmethod
    def link_script_object(script_name:str) -> str:
        """Return a MediaWiki link for script object page."""
        return f"[[SFM:Script-{script_name}|{script_name}]]"


    @staticmethod
    def link_script_member(script_name:str, member_name:str) -> str:
        """Return a MediaWiki link for a script member page."""
        return f"[[SFM:Script-{script_name}/{member_name}|{member_name}]]"
