from enum import Enum
from app.common.collections import KeyedObject


# Types
#---------------------------------------------

class PrimitiveType(Enum):
    VOID = 0
    VAR = 1
    BOOL = 2
    INT = 3
    FLOAT = 4
    STRING = 5


# Script Identifier
#---------------------------------------------

# TODO: Test this on a concrete KeyedCollection.
class ScriptName(KeyedObject):
    """
    Represents a Papyrus script name.
    The value format is `Namespace1:Namespace2:ScriptName`.
    """

    def __init__(self, key:str = ""):
        """Initializes this class with an optional script name value."""
        super().__init__(key)

    @property
    def value(self) -> str:
        """Gets the script name value, which may include namespaces."""
        return self._key

    @value.setter
    def value(self, value:str):
        """Sets the script name value, which may include namespaces."""
        self._key = value.strip() if value else ""

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
