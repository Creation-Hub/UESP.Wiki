import json
import os
from enum import Enum
from typing import Any
from .publishing import PublishOption


class PublishType(Enum):
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
    def decode(data:dict[str, Any], property:str) -> 'PublishType':
        value:str = data.get(property, PublishType.DEFAULT)
        if not value: return PublishType.DEFAULT
        else: return PublishType[value.upper()]


class PublishPapyrus:
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
    def decode(data:dict[str, Any]) -> 'PublishPapyrus':
        identifier:str|None = data.get("identifier")
        if not identifier:
            raise ValueError("An identifier is required.")
        this:PublishPapyrus = PublishPapyrus(identifier)
        this.identifier = identifier
        this.imports = data.get("source.imports", [])
        this.root = data.get("source.directory", "")
        this.publish = PublishOption.json_decode(data)
        return this


class PublishResource:
    def __init__(self) -> None:
        super().__init__()
        self.identifier:str = ""
        self.type:PublishType = PublishType.OFFICIAL
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
        # Jobs\Papyrus
        self.papyrus:dict[str, PublishPapyrus]|None = {}


    @staticmethod
    def decode(identifier:str, data:dict[str, Any]) -> 'PublishResource':
        this:PublishResource = PublishResource()
        this.identifier = identifier
        this.type = PublishType.decode(data, "type")
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
        this.papyrus = PublishResource.decode_papyrus(data, "papyrus")
        return this


    @staticmethod
    def decode_papyrus(data:dict[str, Any], property:str) -> dict[str, PublishPapyrus]|None:
        data_targets:list[Any]|None = data.get(property)
        if not data_targets: return None

        targets:dict[str, PublishPapyrus] = {}
        for data_target in data_targets:
            target:PublishPapyrus = PublishPapyrus.decode(data_target)
            targets[target.identifier] = target
        return targets


class PublishSettings:
    JSON_ENCODING:str = "utf-8"

    def __init__(self) -> None:
        super().__init__()
        self.resources:dict[str, PublishResource] = {}


    @staticmethod
    def load(file_path:str) -> 'PublishSettings':
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")
        with open(file_path, encoding=PublishSettings.JSON_ENCODING) as file:
            data:dict[str, Any] = json.load(file)
        return PublishSettings.decode(data)


    @staticmethod
    def decode(data:dict[str, Any]) -> 'PublishSettings':
        this:PublishSettings = PublishSettings()
        for key, data_provider in data.items():
            provider:PublishResource = PublishResource.decode(key, data_provider)
            this.resources[provider.identifier] = provider
        return this


    @staticmethod
    def json_decode_papyrus(data:dict[str, Any]) -> dict[str, PublishPapyrus]:
        jobs:dict[str, PublishPapyrus] = {}
        for key in data:
            job:PublishPapyrus = PublishPapyrus.decode(data[key])
            jobs[job.identifier] = job
        return jobs
