from typing import Any


class PublishOption:
    """ Publishing options for a project."""

    def __init__(self) -> None:
        super().__init__()

        self.enable:bool = False
        """ Whether to enable any publishing. """

        self.enable_objects:bool = False
        """ Whether to enable publishing of script object pages. """

        self.enable_members:bool = False
        """ Whether to enable publishing of script member pages. """


    @staticmethod
    def json_decode(data_project:dict[str, Any]) -> 'PublishOption':
        this:PublishOption = PublishOption()
        this.enable = data_project.get("publish.enabled", False)
        this.enable_objects = data_project.get("publish.objects", False)
        this.enable_members = data_project.get("publish.members", False)
        return this


class PapyrusTarget:
    """
    Represents a Papyrus project configuration with publishing options.
    See the `PapyrusProject` and `PublishOption` classes.
    """
    def __init__(self, identifier:str) -> None:
        super().__init__()

        self.identifier:str = identifier
        """The indentifier for this configuration."""

        self.root:str = ""
        """The root directory containing Papyrus scripts for this configuration."""

        self.imports:list[str] = []
        """A list of other configuration identifiers to import Papyrus scripts from."""

        self.publish:PublishOption = PublishOption()
        """The publish options for this configuration."""


    @staticmethod
    def decode(data:dict[str, Any]) -> 'PapyrusTarget':
        identifier:str|None = data.get("identifier")
        if not identifier:
            raise ValueError("An identifier is required.")
        this:PapyrusTarget = PapyrusTarget(identifier)
        this.identifier = identifier
        this.imports = data.get("source.imports", [])
        this.root = data.get("source.directory", "")
        this.publish = PublishOption.json_decode(data)
        return this


class PapyrusPackage:
    def __init__(self) -> None:
        super().__init__()
        self.identifier:str = ""
        # Details
        self.name:str = ""
        self.author:str = ""
        self.description:str = ""
        # Site
        self.platform:str = ""
        self.url:str = ""
        self.url_id:str = ""
        # Version
        self.version:str = ""
        self.version_build:str = ""
        self.version_date:str = ""
        # Papyrus
        self.targets:dict[str, PapyrusTarget] = {}


    @staticmethod
    def decode(identifier:str, data:dict[str, Any]) -> 'PapyrusPackage':
        this:PapyrusPackage = PapyrusPackage()
        this.identifier = identifier
        # Details
        this.name = data.get("name", "")
        this.author = data.get("author", "")
        this.description = data.get("description", "")
        # Site
        this.platform = data.get("platform", "")
        this.url = data.get("url", "")
        this.url_id = data.get("url_id", "")
        # Version
        version_data:dict[str, Any] = data.get("version", {})
        this.version = version_data.get("number", "")
        this.version_build = version_data.get("build", "")
        this.version_date = version_data.get("date", "")
        # Papyrus
        this.targets = PapyrusPackage.decode_papyrus(data, "papyrus")
        return this


    @staticmethod
    def decode_papyrus(data:dict[str, Any], property:str) -> dict[str, PapyrusTarget]:
        targets:dict[str, PapyrusTarget] = {}
        data_targets:list[Any]|None = data.get(property)
        if not data_targets: return targets
        for data_target in data_targets:
            target:PapyrusTarget = PapyrusTarget.decode(data_target)
            targets[target.identifier] = target
        return targets
