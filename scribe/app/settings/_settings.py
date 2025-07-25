from ._configuration import Configuration


class AppSettings:
    """
    Represents the application settings.
    """
    def __init__(self) -> None:
        self.configurations:dict[str, Configuration] = {}
        """The app configurations loaded from the settings file."""
