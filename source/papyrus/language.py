from dataclasses import dataclass
from typing import override


# TODO: DEPRECATED! Merge back into ScriptName.
@dataclass(frozen=True)
class KeyedObject:
    """
    DEPRECATED!

    Represents an object that provides a unique identifying key.
    The key is for use with a `KeyedCollection[T]` dictionary abstraction.
    Used to support the intrinsic key strategy for `KeyedCollection`.
    """

    _key:str
    """The unique key for this object."""

    @override
    def __str__(self) -> str:
        """Returns a string that represents the current object."""
        return self._key

    @property
    def key(self) -> str:
        return self._key


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
