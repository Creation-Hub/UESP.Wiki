import os
import json
from typing import Any
from app.context import AppContext
from app.project import PapyrusProject
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
    if os.path.exists(settings_file_path):
        with open(settings_file_path, encoding="utf-8") as file:
            data:dict[str, Any] = json.load(file)
        context.publish_info = data.get("publish", {})
        for data_project in data.get("projects", []):
            project:PapyrusProject = PapyrusProject()
            project.identifier = data_project.get("identifier", "UNNAMED")
            project.imports = data_project.get("source.imports", [])
            project.root = get_property_path(data_project, "source.directory", context.base_directory)
            project.publish.output = get_property_path(data_project, "output.directory", context.base_directory)
            project.publish.sort = get_property_sort(data_project, "output.sort")
            project.publish.enable = data_project.get("output.enabled", False)
            project.publish.enable_objects = data_project.get("output.objects", False)
            project.publish.enable_members = data_project.get("output.members", False)
            context.add(project)
    return context
