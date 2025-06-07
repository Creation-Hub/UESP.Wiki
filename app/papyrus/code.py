class Code:
    """Base class for code elements in a Papyrus script."""
    def __init__(self):
        self.index: int = -1
        """The source code line index for this element."""

        self.definition: str = ""
        """The source code definition for this element (normalized line text)."""

        self.documentation: str = ""
        """The source code documentation for this element."""

        self.game_version: list[str] = []
        """The game version history for this code, starting with when it was introduced."""


class ScriptName:
    """
    Represents a Papyrus script name.
    The value format is `Namespace1:Namespace2:ScriptName`.
    """

    def __init__(self, value: str = ""):
        """Initializes this class with an optional script name value."""
        self._value: str = ""
        self.value = value

    def __str__(self) -> str:
        """Returns the string representation of this class."""
        if self.value: return self.value
        else: return ""

    @property
    def value(self) -> str:
        """Gets the script name value, which may include namespaces."""
        return self._value

    # TODO: Ensure the stored script name value has valid namespace notation and normalization.
    @value.setter
    def value(self, value: str):
        """Sets the script name value, which may include namespaces."""
        self._value = value.strip() if value else ""

    def get_array(self) -> list[str]:
        """Returns the script name as a list of strings."""
        if self.value: return self.value.split(":")
        else: return []

    def set_array(self, name:list[str]) -> bool:
        """Sets the script name from a list of strings."""
        if not name: return False
        self.value = ":".join(name)
        return True

    def file_path(self) -> str:
        """Returns the relative path based on the script name."""
        if not self.value: return ""
        return self.value.replace(":", "\\")

    def file_name(self) -> str:
        """Returns the script file name without extension."""
        if not self.value: return ""
        array = self.get_array()
        return array[-1] if array else ""


# TODO: Possibly consolidate this into the Script() class.
class Header(Code):
    """
    Represents the header of a Papyrus script.
    """

    def __init__(self):
        self.name: ScriptName = ScriptName()
        """The name of this script. Includes the namespace and name."""

        self.extends: ScriptName = ScriptName()
        """The inherited script. Includes the namespace and name."""

        self.flags: list[str] = []
        """The flags associated with the script."""

    def __str__(self) -> str:
        """Returns the string representation of this class."""
        if self.name: return str(self.name)
        else: return ""


# TODO: Consider making the `name` a `list[str]` type to support remote-event syntax.
class Member(Code):
    """
    Represents a member in a Papyrus script.
    This can be a function, property, or event.
    """

    def __init__(self):
        self.name:str = ""
        """The name of the member."""

        self.state: str = ""
        """The state the member belongs to."""

        self.kind: str = ""
        """The kind of member (function, property, event, etc.)."""

        self.type: str = ""
        """The type of the member."""

        self.parameters: list[str] = []
        """The parameters of the member."""

        self.flags: list[str] = []
        """The flags associated with the member."""

        self.game_version: str = ""
        """The game version this member was introduced."""


class Script:
    """Represents a Papyrus script."""

    def __init__(self):
        self.header: Header = Header()
        """The header information of this script."""

        self.members: list[Member] = []
        """The members that belong to this script."""

        self.source_file: str = ""
        """The source file path for this script."""

    def __str__(self) -> str:
        """Returns the string representation of this class."""
        if self.header.name:
            return str(self.header.name)
        else:
            return ""
