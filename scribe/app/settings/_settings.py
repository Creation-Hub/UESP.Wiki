import os
import json
from typing import Any

from scribe.shared.objects import Dump
from ._provider import Provider, ProviderType,ProviderProject
from ._publishing import PublishOption, Sort
from scribe.app.cli import AppArguments

class AppSettings:
    """
    Represents the application settings.
    """
    def __init__(self) -> None:
        # File
        self.file_path:str = ""
        """The json file path for these settings."""

        self.base_directory:str = ""
        """The base directory of the settings file."""

        # Wiki
        self.export_directory:str = ""
        """The export directory for wiki pages."""

        # Generator
        self.providers:dict[str, Provider] = {}
        """The providers loaded from the settings file."""

        # Generator
        self.configurations:dict[str, ProviderProject] = {}
        """The app configurations loaded from the settings file."""

        # Uploader
        self.upload_configuration_file:str|None = None
        """The json file path for the uploader configuration file."""

        # Uploader
        self.environment:str|None = None
        """The environment to use for the uploader."""


    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create(arguments:AppArguments) -> 'AppSettings':
        if not arguments.configuration_file:
            raise ValueError("No configuration file provided in arguments.")

        # Read the settings from the provided configuration file.
        this:AppSettings = AppSettings._read(arguments.configuration_file)

        # Apply any command line arguments to the settings.
        this.upload_configuration_file = arguments.upload_configuration_file or this.upload_configuration_file
        this.environment = arguments.upload_environment or this.environment

        return this


    @staticmethod
    def _read(file_path:str) -> 'AppSettings':
        """
        Reads the given application settings file.
        """
        # Ensure the settings file exists.
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")

        # Read data from the settings file.
        with open(file_path, encoding="utf-8") as file:
            data:dict[str, Any] = json.load(file)

        settings:AppSettings = AppSettings()
        settings.file_path = os.path.abspath(file_path)
        settings.base_directory = os.path.dirname(settings.file_path)
        settings.export_directory = AppSettings._json_get_property_path(data, "export.directory", settings.base_directory)

        # Read the provider configurations.
        data_providers:list[Any] = data.get("providers", [])
        for data_provider in data_providers:
            data_provider:dict[str, Any] = data_provider
            provider:Provider = AppSettings._json_read_Provider(data_provider)
            settings.providers[provider.identifier] = provider

            # Read the configuration for projects.
            data_projects:list[Any] = data_provider.get("projects", [])
            for data_project in data_projects:
                data_project:dict[str, Any] = data_project
                configuration:ProviderProject = AppSettings._json_read_Configuration(data_project, settings.base_directory)
                settings.configurations[configuration.identifier] = configuration

        # Return the application settings.
        return settings


    @staticmethod
    def _json_read_Provider(data_provider:dict[str, Any]) -> Provider:
        provider:Provider = Provider()
        provider.identifier = data_provider.get("identifier", "")
        provider.type = AppSettings._json_get_property_provider_type(data_provider, "type")
        # Details
        provider.name = data_provider.get("name", "")
        provider.author = data_provider.get("author", "")
        provider.description = data_provider.get("description", "")
        # Site
        provider.platform = data_provider.get("platform", "")
        provider.url = data_provider.get("url", "")
        provider.url_id = data_provider.get("url_id", "")
        # Version
        version_data:dict[str, Any] = data_provider.get("version", {})
        provider.version = version_data.get("number", "")
        provider.version_build = version_data.get("version_build", "")
        provider.version_date = version_data.get("version_date", "")
        return provider


    @staticmethod
    def _json_read_Configuration(data_project:dict[str, Any], base_directory:str) -> ProviderProject:
        configuration:ProviderProject = ProviderProject()
        configuration.identifier = data_project.get("identifier", "UNNAMED")
        configuration.imports = data_project.get("source.imports", [])
        configuration.root = AppSettings._json_get_property_path(data_project, "source.directory", base_directory)
        configuration.publish = AppSettings._json_read_PublishOption(data_project, base_directory)
        return configuration


    @staticmethod
    def _json_read_PublishOption(data_project:dict[str, Any], base_directory:str) -> PublishOption:
        publish:PublishOption = PublishOption()
        publish.output = AppSettings._json_get_property_path(data_project, "output.directory", base_directory)
        publish.sort = AppSettings._json_get_property_sort(data_project, "output.sort")
        publish.enable = data_project.get("output.enabled", False)
        publish.enable_objects = data_project.get("output.objects", False)
        publish.enable_members = data_project.get("output.members", False)
        return publish


    @staticmethod
    def _json_get_property_path(data:dict[str, Any], property:str, directory:str) -> str:
        path:str = data.get(property, "")
        if not path: return ""
        elif os.path.isabs(path): return path
        else: return os.path.join(directory, path)


    @staticmethod
    def _json_get_property_sort(data:dict[str, Any], property:str) -> Sort:
        value:str = data.get(property, Sort.DEFAULT.name)
        if not value: return Sort.DEFAULT
        else: return Sort[value.upper()]


    @staticmethod
    def _json_get_property_provider_type(data:dict[str, Any], property:str) -> ProviderType:
        value:str = data.get(property, ProviderType.DEFAULT)
        if not value: return ProviderType.DEFAULT
        else: return ProviderType[value.upper()]
