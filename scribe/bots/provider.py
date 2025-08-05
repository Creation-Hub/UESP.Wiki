from enum import Enum
from typing import Any
from .publishing import PublishOption


class ProviderProject:
    """
    Represents a Papyrus project configuration with publishing options.
    See the `PapyrusProject` and `PublishOption` classes.
    """
    def __init__(self) -> None:
        self.identifier:str = ""
        """The indentifier for this configuration."""

        self.root:str = ""
        """The root directory containing Papyrus scripts for this configuration."""

        self.imports:list[str] = []
        """A list of other configuration identifiers to import Papyrus scripts from."""

        self.publish:PublishOption = PublishOption()
        """The publish options for this configuration."""


    @staticmethod
    def json_decode(data_project:dict[str, Any]) -> 'ProviderProject':
        this:ProviderProject = ProviderProject()
        this.identifier = data_project.get("identifier", "UNNAMED")
        this.imports = data_project.get("source.imports", [])
        this.root = data_project.get("source.directory", "")
        this.publish = PublishOption.json_decode(data_project)
        return this


class ProviderType(Enum):
    DEFAULT = "default"
    """The default provider type."""

    OFFICIAL = "official"
    """A provider for Official sources."""

    CREATION = "creation"
    """A provider for Creations sources."""

    COMMUNITY = "community"
    """A provider for Community libraries."""

    SAMPLE = "sample"
    """A provider for wiki samples."""

    TEST = "test"
    """A provider for developer testing."""

    @staticmethod
    def json_decode(data:dict[str, Any], property:str) -> 'ProviderType':
        value:str = data.get(property, ProviderType.DEFAULT)
        if not value: return ProviderType.DEFAULT
        else: return ProviderType[value.upper()]


class Provider:
    """
    Represents information about the provider.
    """
    def __init__(self) -> None:
        self.identifier:str = ""
        self.type:ProviderType = ProviderType.OFFICIAL
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


    @staticmethod
    def json_decode(data_provider:dict[str, Any]) -> 'Provider':
        this:Provider = Provider()
        this.identifier = data_provider.get("identifier", "")
        this.type = ProviderType.json_decode(data_provider, "type")
        # Details
        this.name = data_provider.get("name", "")
        this.author = data_provider.get("author", "")
        this.description = data_provider.get("description", "")
        # Site
        this.platform = data_provider.get("platform", "")
        this.url = data_provider.get("url", "")
        this.url_id = data_provider.get("url_id", "")
        # Version
        version_data:dict[str, Any] = data_provider.get("version", {})
        this.version = version_data.get("number", "")
        this.version_build = version_data.get("version_build", "")
        this.version_date = version_data.get("version_date", "")
        return this
