import os
import json
from typing import Any
from app.configuration import Configuration
from app.context import AppContext
from app.papyrus.project import PapyrusProject
from app.publishing import PublishOption
from app.publishing import Sort


# Json
#---------------------------------------------

def get_property_path(data:dict[str, Any], property:str, directory:str) -> str:
    path = data.get(property, None)
    # os.path.abspath(path)
    if not path: return ""
    elif os.path.isabs(path): return path
    else: return os.path.join(directory, path)


def get_property_sort(data:dict[str, Any], property:str) -> Sort:
    value = data.get(property, None)
    if value is None: return Sort.DEFAULT
    try: return Sort[value.upper()]
    except KeyError: return Sort.DEFAULT


# Settings
#---------------------------------------------

def read(settings_file_path:str) -> AppContext:
    """
    Reads application settings file.
    """
    context:AppContext = AppContext()
    context.base_directory = os.path.dirname(os.path.abspath(settings_file_path))

    # Ensure the settings file exists.
    if os.path.exists(settings_file_path):
        # Read data from the settings file.
        with open(settings_file_path, encoding="utf-8") as file:
            data:dict[str, Any] = json.load(file)

        # Read the configuration for the application.
        context.export_directory = get_property_path(data, "export.directory", context.base_directory)
        context.publish_info = data.get("publish", {})

        # Read the configuration for projects.
        for data_project in data.get("projects", []):
            # Get the identifier for the project.
            identifier:str = data_project.get("identifier", "UNNAMED")

            # Create the Papyrus project.
            project:PapyrusProject = PapyrusProject()
            project.identifier = identifier
            project.imports = data_project.get("source.imports", [])
            project.root = get_property_path(data_project, "source.directory", context.base_directory)

            # Create the Publish options.
            publish:PublishOption = PublishOption()
            publish.output = get_property_path(data_project, "output.directory", context.base_directory)
            publish.sort = get_property_sort(data_project, "output.sort")
            publish.enable = data_project.get("output.enabled", False)
            publish.enable_objects = data_project.get("output.objects", False)
            publish.enable_members = data_project.get("output.members", False)

            # Create the configuration to the context.
            configuration:Configuration = Configuration()
            configuration.identifier = identifier
            configuration.project = project
            configuration.publish = publish
            context.configurations[configuration.identifier] = configuration

            # Add the project to the context.
            context.add(project)

    # Return the application context.
    return context
