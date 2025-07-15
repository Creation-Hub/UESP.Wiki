from typing import Any
from app.settings import Configuration
from app.papyrus.project import PapyrusContext


class AppContext:
    def __init__(self) -> None:
        self.base_directory:str = ""
        """The base directory of the settings file."""

        self.export_directory:str = ""
        """The export directory for wiki pages."""

        self.publish_info:dict[str, Any] = {}
        """Information about the game and editor for publishing."""

        self.configurations:dict[str, Configuration] = {}
        """The app configurations loaded from the settings file."""

        self.papyrus:PapyrusContext = PapyrusContext()
        """The Papyrus context for script analysis."""
