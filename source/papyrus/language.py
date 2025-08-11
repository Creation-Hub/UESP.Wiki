from typing import override
from sharp.collections import KeyedObject

# TODO: Test this on a concrete KeyedCollection.
class ScriptName(KeyedObject):
    """
    Represents a Papyrus script name.
    The value format is `Namespace1:Namespace2:ScriptName`.
    """

    def __init__(self, key:str = "") -> None:
        """Initializes this class with an optional script name value."""
        KeyedObject.__init__(self, key)


    @property
    @override
    def key(self) -> str:
        """Gets the script name value, which may include namespaces."""
        return self._key


    def get_array(self) -> list[str]:
        """Returns the script name as a list of strings."""
        if self.key: return self.key.split(":")
        else: return []


    @staticmethod
    def from_array(name:list[str]) -> 'ScriptName|None':
        """Creates a script name from a list of strings."""
        if not name: return None
        key:str = ":".join(name)
        return ScriptName(key)


    def file_path(self) -> str:
        """Returns the relative path based on the script name."""
        if not self.key: return ""
        return self.key.replace(":", "\\")


    def file_name(self) -> str:
        """Returns the script file name without extension."""
        if not self.key: return ""
        array = self.get_array()
        return array[-1] if array else ""
