from typing import Any, Dict
from app.settings import Configuration
from app.papyrus.project import PapyrusContext
from app.papyrus.project import PapyrusProject


# Context
#---------------------------------------------

class AppContext:
    def __init__(self):
        self.base_directory:str = ""
        """The base directory of the settings file."""

        self.export_directory:str = ""
        """The export directory for wiki pages."""

        self.publish_info:dict[str, Any] = {}
        """Information about the game and editor for publishing."""

        self.configurations:Dict[str, Configuration] = {}
        self.papyrus:PapyrusContext = PapyrusContext()


    def add(self, project:PapyrusProject):
        """Adds a project to the application context."""
        self.papyrus.add(project)
