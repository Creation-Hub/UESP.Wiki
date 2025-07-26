import os
import json
from typing import Any
from ._configuration import Configuration
from ._publishing import PublishOption, Sort


class AppSettings:
    """
    Represents the application settings.
    """
    def __init__(self) -> None:
        self.file_path:str = ""
        """The settings file path to use."""

        self.base_directory:str = ""
        """The base directory of the settings file."""

        self.export_directory:str = ""
        """The export directory for wiki pages."""

        self.environment:str|None = None
        """The environment to use for the application uploader."""

        self.publish_info:dict[str, Any] = {}
        """OBSOLETE: Information about the game and editor for publishing."""

        self.configurations:dict[str, Configuration] = {}
        """The app configurations loaded from the settings file."""

        self.game_info:dict[str, Any] = {}
        """OBSOLETE: Information about the game for publishing."""

        self.editor_info:dict[str, Any] = {}
        """OBSOLETE: Information about the editor for publishing."""


# Json
#---------------------------------------------

def get_property_path(data:dict[str, Any], property:str, directory:str) -> str:
    path:str = data.get(property, "")
    if not path: return ""
    elif os.path.isabs(path): return path
    else: return os.path.join(directory, path)


def get_property_sort(data:dict[str, Any], property:str) -> Sort:
    value:str = data.get(property, "DEFAULT")
    if not value: return Sort.DEFAULT
    else: return Sort[value.upper()]


# Settings
#---------------------------------------------

def read(file_path:str) -> AppSettings:
    """
    Reads the given application settings file.
    """
    settings:AppSettings = AppSettings()
    settings.file_path = os.path.abspath(file_path)
    settings.base_directory = os.path.dirname(settings.file_path)

    # Ensure the settings file exists.
    if os.path.exists(file_path):
        # Read data from the settings file.
        with open(file_path, encoding="utf-8") as file:
            data:dict[str, Any] = json.load(file)

        # Read the configuration for the application.
        settings.export_directory = get_property_path(data, "export.directory", settings.base_directory)
        settings.publish_info = data.get("publish", {})

        # Get content data for game and editor.
        settings.game_info = settings.publish_info.get("game", {})
        settings.editor_info = settings.publish_info.get("editor", {})

        # Read the configuration for projects.
        for data_project in data.get("projects", []):
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

            # Create the configuration to the context.
            configuration:Configuration = Configuration()
            configuration.identifier = identifier
            configuration.imports = data_project.get("source.imports", [])
            configuration.root = get_property_path(data_project, "source.directory", settings.base_directory)
            configuration.publish = publish

            # Add the configuration to the settings.
            settings.configurations[configuration.identifier] = configuration

    # Return the application settings.
    return settings
