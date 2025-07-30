import os
import json
from typing import Any
from .provider import Provider, ProviderType
from ._configuration import Configuration
from ._publishing import PublishOption, Sort


# Json
#---------------------------------------------

def get_property_path(data:dict[str, Any], property:str, directory:str) -> str:
    path:str = data.get(property, "")
    if not path: return ""
    elif os.path.isabs(path): return path
    else: return os.path.join(directory, path)


def get_property_sort(data:dict[str, Any], property:str) -> Sort:
    value:str = data.get(property, Sort.DEFAULT.name)
    if not value: return Sort.DEFAULT
    else: return Sort[value.upper()]


def get_property_provider_type(data:dict[str, Any], property:str) -> ProviderType:
    value:str = data.get(property, ProviderType.DEFAULT)
    if not value: return ProviderType.DEFAULT
    else: return ProviderType[value.upper()]


# Settings
#---------------------------------------------

class AppSettings:
    """
    Represents the application settings.
    """
    def __init__(self) -> None:
        self.file_path:str = ""
        """The json file path for these settings."""

        self.base_directory:str = ""
        """The base directory of the settings file."""

        self.export_directory:str = ""
        """The export directory for wiki pages."""

        self.environment:str|None = None
        """The environment to use for the uploader."""

        self.providers:dict[str, Provider] = {}
        """The providers loaded from the settings file."""

        self.configurations:dict[str, Configuration] = {}
        """The app configurations loaded from the settings file."""


    @staticmethod
    def read(file_path:str) -> 'AppSettings':
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

        # Read the configuration for the application.
        settings.export_directory = get_property_path(data, "export.directory", settings.base_directory)

        for data_provider in data.get("providers", []):
            data_provider:dict[str, Any] = data_provider

            provider:Provider = Provider()
            provider.identifier = data_provider.get("identifier", "")
            provider.type = get_property_provider_type(data_provider, "type")
            provider.name = data_provider.get("name", "")
            provider.author = data_provider.get("author", "")
            provider.description = data_provider.get("description", "")
            provider.platform = data_provider.get("platform", "")
            provider.url = data_provider.get("url", "")
            provider.url_id = data_provider.get("url_id", "")

            version_data:dict[str, Any] = data_provider.get("version", {})
            provider.version = version_data.get("number", "")
            provider.version_build = version_data.get("version_build", "")
            provider.version_date = version_data.get("version_date", "")
            # Add provider to the settings.
            settings.providers[provider.identifier] = provider

            # Read the configuration for projects.
            for data_project in data_provider.get("projects", []):
                data_project:dict[str, Any] = data_project

                # Get the identifier for this configuration.
                identifier:str = data_project.get("identifier", "UNNAMED")

                # Create the Publish options.
                publish:PublishOption = PublishOption()
                publish.output = get_property_path(data_project, "output.directory", settings.base_directory)
                publish.sort = get_property_sort(data_project, "output.sort")
                publish.enable = data_project.get("output.enabled", False)
                publish.enable_objects = data_project.get("output.objects", False)
                publish.enable_members = data_project.get("output.members", False)

                # Create the configuration.
                configuration:Configuration = Configuration()
                configuration.identifier = identifier
                configuration.imports = data_project.get("source.imports", [])
                configuration.root = get_property_path(data_project, "source.directory", settings.base_directory)
                configuration.publish = publish

                # Add the configuration to the settings.
                settings.configurations[configuration.identifier] = configuration

        # Return the application settings.
        return settings
