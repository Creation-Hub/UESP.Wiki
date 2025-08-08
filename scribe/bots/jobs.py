from enum import Enum
from typing import Any
from scribe.shared.collections import KeyedObject
from .publishing import PublishOption


class JobType(Enum):
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
    def json_decode(data:dict[str, Any], property:str) -> 'JobType':
        value:str = data.get(property, JobType.DEFAULT)
        if not value: return JobType.DEFAULT
        else: return JobType[value.upper()]


class Job(KeyedObject):
    """
    Represents a Papyrus project configuration with publishing options.
    See the `PapyrusProject` and `PublishOption` classes.
    """
    def __init__(self, identifier:str) -> None:
        super().__init__(identifier)

        self.identifier:str = ""
        """The indentifier for this configuration."""

        self.root:str = ""
        """The root directory containing Papyrus scripts for this configuration."""

        self.imports:list[str] = []
        """A list of other configuration identifiers to import Papyrus scripts from."""

        self.publish:PublishOption = PublishOption()
        """The publish options for this configuration."""


    @staticmethod
    def json_decode(data:dict[str, Any]) -> 'Job':
        identifier:str|None = data.get("identifier")
        if not identifier:
            raise ValueError("An identifier is required.")
        this:Job = Job(identifier)
        this.identifier = identifier
        this.imports = data.get("source.imports", [])
        this.root = data.get("source.directory", "")
        this.publish = PublishOption.json_decode(data)
        return this


class JobOwner:
    """
    Represents information about the provider.
    """
    def __init__(self) -> None:
        super().__init__()
        self.identifier:str = ""
        self.type:JobType = JobType.OFFICIAL
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
        self.jobs:dict[str, Job]|None = {}


    @staticmethod
    def json_decode(data:dict[str, Any]) -> 'JobOwner':
        this:JobOwner = JobOwner()
        this.identifier = data.get("identifier", "")
        this.type = JobType.json_decode(data, "type")
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
        # Jobs\Papyrus
        this.jobs = JobOwner.json_decode_jobs(data, "jobs")
        return this


    @staticmethod
    def json_decode_jobs(data:dict[str, Any], property:str) -> dict[str, Job]|None:
        jobs:dict[str, Job] = {}
        data_jobs:list[Any]|None = data.get(property)
        if not data_jobs: return None
        for data_job in data_jobs:
            data_job:dict[str, Any] = data_job
            job:Job = Job.json_decode(data_job)
            jobs[job.identifier] = job
        return jobs
