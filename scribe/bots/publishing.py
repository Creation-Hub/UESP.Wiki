from enum import Enum
from typing import Any


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

    @staticmethod
    def json_decode(data:dict[str, Any], property:str) -> 'Sort':
        value:str = data.get(property, Sort.DEFAULT.name)
        if not value: return Sort.DEFAULT
        else: return Sort[value.upper()]


class PublishOption:
    """ Publishing options for a project."""

    def __init__(self) -> None:
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


    @staticmethod
    def json_decode(data_project:dict[str, Any]) -> 'PublishOption':
        this:PublishOption = PublishOption()
        this.output = data_project.get("output.directory", "")
        this.sort = Sort.json_decode(data_project, "output.sort")
        this.enable = data_project.get("output.enabled", False)
        this.enable_objects = data_project.get("output.objects", False)
        this.enable_members = data_project.get("output.members", False)
        return this
