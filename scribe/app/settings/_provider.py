from enum import Enum
from ._publishing import PublishOption


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
