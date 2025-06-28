from typing import Dict
from app.papyrus.language import ScriptName


# Source Code
#---------------------------------------------

class Code:
    """A base class for source code elements in a Papyrus script."""
    def __init__(self):
        self.index:int = -1
        """The source code line index for this element."""

        self.definition:str = ""
        """The source code definition for this element (normalized line text)."""

        self.documentation:str = ""
        """The source code documentation for this element."""

        self.game_version:list[str] = []
        """The game version history for this code, starting with when it was introduced."""


# Elements
#---------------------------------------------

class Element(Code):
    """
    Represents an element of a Papyrus script.
    """
    def __init__(self):
        super().__init__()

        self.name:str = ""
        """The name of this element."""

        self.flags:list[str] = []
        """The flags associated with this element."""

        self._kind:str = ""
        """The kind of element (function, property, event, etc.)."""

    @property
    def kind(self) -> str:
        """Gets the canonical Papyrus type name (kind) for this member."""
        return self._kind


# Element Attributes
#---------------------------------------------

class ValueTypeAttribute():
    def __init__(self):
        self.type:str = ""
        """The member type is used for variables, properties, and the return type for functions."""

class ValueAutoAttribute():
    def __init__(self):
        self.value_auto:str = ""
        """The field initialized auto value for this member."""

class ParameterAttribute():
    def __init__(self):
        self.parameters:list[str] = []
        """The parameters of this member."""


# Header
#---------------------------------------------

class Header(Code):
    """
    Represents the header of a Papyrus script.
    """
    def __init__(self):
        super().__init__()

        # TODO: This overlaps with the inherited element name.
        self.name:ScriptName = ScriptName()
        """The name of this script. Includes the namespace and name."""

        self.extends:ScriptName = ScriptName()
        """The inherited script. Includes the namespace and name."""

        # TODO: Refactor this to use a common attribute.
        self.flags:list[str] = []
        """The flags associated with the script."""

    def __str__(self) -> str:
        """Returns the string representation of this class."""
        if self.name: return str(self.name)
        else: return ""


class Member(Element):
    def __init__(self):
        super().__init__()

        # TODO: Move to PropertyGroup class.
        self.group:str = ""
        """The group this member belongs to, if any. This only applies to properties."""

        # TODO: Move to PropertyGroup class.
        self.group_flags:str = ""
        """The flags associated with the group this member belongs to, if any."""


# Members
#---------------------------------------------

class Guard(Member):
    def __init__(self):
        super().__init__()
        self._kind = "Guard"


class Variable(Member, ValueTypeAttribute, ValueAutoAttribute):
    def __init__(self):
        super().__init__()
        ValueTypeAttribute.__init__(self)
        ValueAutoAttribute.__init__(self)
        self._kind = ""


class Structure(Member):
    def __init__(self):
        super().__init__()
        self._kind = "Struct"
        self.variables:Dict[str, Variable] = {}


# Properties
#---------------------------------------------

class Property(Member, ValueTypeAttribute, ValueAutoAttribute):
    def __init__(self):
        super().__init__()
        ValueTypeAttribute.__init__(self)
        ValueAutoAttribute.__init__(self)
        self._kind = "Property"
        self.getter:Function|None = None
        self.setter:Function|None = None

    def isAuto(self) -> bool:
        return "Auto" in self.flags or "AutoReadOnly" in self.flags


class PropertyGroup(Code):
    def __init__(self):
        super().__init__()
        self.kind = "Group"
        self.properties:Dict[str, Property] = {}


# Methods
#---------------------------------------------

class Function(Member, ParameterAttribute, ValueTypeAttribute):
    def __init__(self):
        super().__init__()
        ParameterAttribute.__init__(self)
        ValueTypeAttribute.__init__(self)
        self._kind = "Function"


class Event(Member, ParameterAttribute):
    def __init__(self):
        super().__init__()
        ParameterAttribute.__init__(self)
        self._kind = "Event"
        self.isRemote:bool = False
        """Indicates if this event is a remote event handler."""

class State(Code):
    def __init__(self):
        super().__init__()
        self._kind = "State"
        self.methods:Dict[str, Function|Event] = {}


# Script
#---------------------------------------------

class Script:
    """Represents a Papyrus script."""

    def __init__(self):
        self.header:Header = Header()
        """The header information of this script."""

        # TODO: Refactor this into a dictionary of members.
        self.members:list[Member] = []
        """The members that belong to this script."""

    def __str__(self) -> str:
        """Returns the string representation of this class."""
        if self.header.name:
            return str(self.header.name)
        else:
            return ""
