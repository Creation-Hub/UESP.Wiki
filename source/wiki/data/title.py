"""
- https://www.mediawiki.org/wiki/Help:Links
- https://www.mediawiki.org/wiki/Manual:Page_ID
- https://www.mediawiki.org/wiki/Manual:Page_title
- https://www.mediawiki.org/wiki/Manual:Title.php

A page whose name is not prefixed by a namespace lies in the mainspace.

Note, however, that colons and prefixes can also appear in page titles without indicating a namespace:
    the page `Foo:Namespaces` is a page located in the mainspace because the namespace 'Foo' does not exist.

Similarly the page `Help:Foo:Namespaces` is in the 'Help' namespace.

prefix:	namespace:	page name
optional	optional	required
"""
from typing import Any, override
from dataclasses import dataclass
from .namespaces import Namespace

@dataclass(frozen=True)
class Title:
    """
    Represents a MediaWiki article title.
    The class data is immutable.
    """

    name:str
    """The article name."""

    namespace:Namespace = Namespace("", None)
    """The article namespace."""


    def __post_init__(self) -> None:
        if self.name == "":
            raise ValueError("The `name` cannot be empty.")
        name:str = self.name.rstrip().replace(" ", "_")
        object.__setattr__(self, "name", name)


    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, namespace={self.namespace!r})"


    @override
    def __str__(self) -> str:
        return self.display


    @property
    def display(self) -> str:
        """The display version of the title, with spaces instead of underscores."""
        return self.name.replace("_", " ")


    @property
    def value(self) -> str:
        """The full title value including namespace prefix if applicable."""
        if self.namespace.name == "":
            return self.name
        else:
            return f"{self.namespace.name}:{self.name}"


    @property
    def link(self) -> str:
        if self.namespace.alias:
            return f"[[{self.namespace.alias}:{self.name}]]"
        elif self.namespace.name:
            return f"[[{self.namespace.name}:{self.name}]]"
        else:
            return f"[[{self.name}]]"


    @property
    def link_visible(self) -> str:
        if self.namespace.alias:
            return f"[[:{self.namespace.alias}:{self.name}|{self.display}]]"
        elif self.namespace.name:
            return f"[[:{self.namespace.name}:{self.name}|{self.display}]]"
        else:
            return f"[[:{self.name}]]"



class ArticleTitleJson:

    @staticmethod
    def encode(this:Title) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "name": this.name,
            "namespace": this.namespace.data_encode()
        }
        return data


    @staticmethod
    def decode(data:dict[str, Any]) -> Title:
        """The data decoder for this class."""
        name:str|None = data.get("name")
        if name is None or name == "":
            raise ValueError("Title must have a valid name.")

        namespace:Namespace|None = data.get("namespace")
        if namespace is None:
            raise ValueError("Title must have a valid namespace.")

        return Title(name, namespace)
