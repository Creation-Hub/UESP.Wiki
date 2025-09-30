"""
Provides constants for the UESP Wiki.
"""
from wiki.data.common import Namespaces
from wiki.data.namespaces import Namespace
from wiki.data.title import Title

class Wiki:
    """
    This class contains constants that are used throughout the wiki generation process.
    These fields should be considered TODO for implementating with configurable options.
    """

    # Common
    #---------------------------------------------

    INFOBOX_TEMPLATES_CATEGORY:Title = Title("Infobox_Templates", Namespaces.Category)
    """
    The category for article-templates that provide information boxes.
    This string is used in the template definition directly and does not have internal link syntax.
    """


    # SFM
    #---------------------------------------------

    SFM_NAMESPACE:Namespace = Namespace("Starfield_Mod", "SFM")
    """
    The top-level namespace for modding related articles.
    This is used within page content to categorize articles related to modding.

    This DOES have internal link syntax.
    ex: `[[SFM:Script-MyScript]]`

    https://starfieldwiki.net/wiki/Starfield_Mod:Main_Page
    """


    SFM_CATEGORY:Title = Title("Starfield_Mod", Namespaces.Category)
    """
    The top-level category for modding related articles.
    https://starfieldwiki.net/wiki/Category:Starfield_Mod
    """


    # Mods
    #---------------------------------------------

    MODS_CATEGORY:Title = Title("Starfield_Mod-Mods", Namespaces.Category)
    """
    https://starfieldwiki.net/wiki/Category:Starfield_Mod-Mods
    """

    MODS:Title = Title("Mods", SFM_NAMESPACE)
    """
    https://starfieldwiki.net/wiki/Starfield_Mod:Mods
    """

    DLC:Title = Title("Included_DLCs", SFM_NAMESPACE)
    """
    https://starfieldwiki.net/wiki/Starfield_Mod:Included_DLCs
    """

    VCP:Title = Title("Verified_Creator_Program", SFM_NAMESPACE)
    """
    https://starfieldwiki.net/wiki/Starfield_Mod:Verified_Creator_Program
    """


    # Modding
    #---------------------------------------------

    MODDING_CATEGORY:Title = Title("Starfield_Mod-Modding", Namespaces.Category)
    """
    The category for articles related to mod creation.

    https://starfieldwiki.net/wiki/Category:Starfield_Mod-Modding
    """


    # Papyrus
    #---------------------------------------------

    PAPYRUS_CATEGORY:Title = Title("Starfield_Mod-Papyrus", Namespaces.Category)
    """
    The category for Papyrus scripts and related articles.
    This is used within page content to categorize articles related to Papyrus scripts.
    This DOES have internal link syntax.

    ex: `[[Category:Starfield_Mod-Papyrus]]`
    """


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
