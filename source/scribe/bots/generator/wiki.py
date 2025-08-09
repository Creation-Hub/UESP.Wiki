# ============================================
# TEMPORARY HACK - MOVE TO PROPER DOMAIN MODEL
# ============================================

from wiki.data.article import Category


class Wiki:
    """
    Constants for the UESP Wiki.
    This class contains constants that are used throughout the wiki generation process.
    These fields should be considered TODO for implementating with configurable options.
    """

    # Namespaces
    #---------------------------------------------

    NAMESPACE_MODDING:str = "Starfield_Mod"
    """The namespace for modding related articles."""

    NS_MODDING:str = "SFM"
    """
    The shorthand alias for the modding namespace.
    Should only be used when referencing the page, not page creation.
    """


    # Categories
    #---------------------------------------------

    CATEGORY_TEMPLATES_INFOBOX:Category = Category()
    """
    The category for article-templates that provide information boxes.
    This string is used in the template definition directly and does not have internal link syntax.
    """
    CATEGORY_TEMPLATES_INFOBOX.name = "Infobox_Templates"



    CATEGORY_PAPYRUS:Category = Category()
    """
    The category for Papyrus scripts and related articles.
    This is used within page content to categorize articles related to Papyrus scripts.
    This DOES have internal link syntax.

    ex: `[[Category:Starfield_Mod-Papyrus]]`
    """
    CATEGORY_PAPYRUS.name = "Starfield_Mod-Papyrus"


    # Methods
    #---------------------------------------------

    @staticmethod
    def link_script_object(script_name:str) -> str:
        """Return a MediaWiki link for script object page."""
        return f"[[SFM:Script-{script_name}|{script_name}]]"


    @staticmethod
    def link_script_member(script_name:str, member_name:str) -> str:
        """Return a MediaWiki link for a script member page."""
        return f"[[SFM:Script-{script_name}/{member_name}|{member_name}]]"
