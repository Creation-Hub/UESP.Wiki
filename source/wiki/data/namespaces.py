"""
- https://www.mediawiki.org/wiki/Help:Namespaces
- https://www.mediawiki.org/wiki/Help:Magic_words#Namespaces
- https://www.mediawiki.org/wiki/Help:Namespaces#Namespace_aliases
- https://www.mediawiki.org/wiki/Manual:Namespace
- https://www.mediawiki.org/wiki/Manual:Namespace_constants
- https://www.mediawiki.org/wiki/Manual:Using_custom_namespaces
- https://www.mediawiki.org/wiki/Manual:Defines.php
- https://www.mediawiki.org/wiki/Extension_default_namespaces
"""
from typing import Any, override
from dataclasses import dataclass

@dataclass(frozen=True)
class Namespace:
    """
    Represents a MediaWiki namespace.
    The class data is immutable.
    """

    name:str
    """The name of this namespace."""

    alias:str|None = None
    """An optional alias for this namespace, used for shorthand links."""


    def __post_init__(self) -> None:
        name:str = self.name.strip().replace(" ", "_")
        object.__setattr__(self, "name", name)
        if self.alias:
            alias:str = self.alias.strip().replace(" ", "_")
            object.__setattr__(self, "alias", alias)


    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, alias={self.alias!r})"


    @override
    def __str__(self) -> str:
        if self.alias: return self.alias
        else: return self.name


    def data_encode(self) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {}
        data["name"] = self.name
        if self.alias is not None:
            data["alias"] = self.alias
        return data


    @staticmethod
    def data_decode(data:dict[str, Any]) -> 'Namespace':
        """The data decoder for this class."""
        name:str|None = data.get("name")
        if name is None or name == "":
            raise ValueError("Namespace must have a valid name.")
        alias:str|None = data.get("alias")
        return Namespace(name, alias)
