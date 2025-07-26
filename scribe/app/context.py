from scribe.app.settings import AppSettings
from scribe.papyrus.project import PapyrusContext


class AppContext:
    def __init__(self) -> None:
        self.settings:AppSettings = AppSettings()
        """The application settings object."""

        self.papyrus:PapyrusContext = PapyrusContext()
        """The Papyrus context for script analysis."""
