from enum import Enum

class Sort(Enum):
    """
    Sorting options for the output wiki pages.
    """
    DEFAULT = 1
    """
    Default sorting, uses the script's namespace and name.

    Example: `Base-Native\\MyNamespace\\Action.wiki`
    """
    FLAT = 2
    """
    Flat sorting, uses the script's namespace and name with a hyphen.

    Example: `Base-Native\\MyNamespace-Action.wiki`
    """
    TREE = 3
    """
    Tree sorting, uses the script's namespace and name in a folder structure.

    Example: `Base-Native\\MyNamespace\\Action\\Action.wiki`
    """

class PublishOption:
    def __init__(self):
        self.output:str = ""
        """ The output directory for the project wiki pages. """
        self.sort:Sort = Sort.DEFAULT
        """ The sorting option for the output wiki pages. """
        self.enable:bool = False
        """ Whether to enable any publishing. """
        self.enable_objects:bool = False
        """ Whether to enable publishing of script object pages. """
        self.enable_members:bool = False
        """ Whether to enable publishing of script member pages. """
