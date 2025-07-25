from ._publishing import PublishOption


class Configuration:
    def __init__(self) -> None:
        self.identifier:str = ""
        """The indentifier for this configuration."""

        self.root:str = ""
        """The root directory containing Papyrus scripts for this configuration."""

        self.imports:list[str] = []
        """A list of other configuration identifiers to import Papyrus scripts from."""

        self.publish:PublishOption = PublishOption()
        """The publish options for this configuration."""
