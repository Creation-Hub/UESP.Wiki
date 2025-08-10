import re
from collections import ChainMap

class Normalize:
    """
    Text normalization utilities for Papyrus source code.

    Provides functions to clean and standardize Papyrus text elements.
    """

    # Canonical Name Mappings
    #---------------------------------------------

    MAP_KEYWORDS:dict[str, str] = {
        "SCRIPTNAME": "ScriptName",
        "EXTENDS": "Extends",
        "STATE": "State",
        "FUNCTION": "Function",
        "EVENT": "Event",
        "PROPERTY": "Property",
        "STRUCT": "Struct",
        "GUARD": "Guard",
        "SELF": "self",
        "PARENT": "parent",
        "CUSTOMEVENT": "CustomEvent"
    }

    MAP_FLAGS:dict[str, str] = {
        "NATIVE": "Native",
        "CONST": "Const",
        "HIDDEN": "Hidden",
        "CONDITIONAL": "Conditional",
        "DEFAULT": "Default",
        "SELFONLY": "SelfOnly",
        "PRIVATE": "Private",
        "PROTECTED": "Protected",
        "GLOBAL": "Global",
        "AUTO": "Auto",
        "MANDATORY": "Mandatory",
        "READONLY": "ReadOnly",
        "DEBUGONLY": "DebugOnly",
        "BETAONLY": "BetaOnly"
    }

    MAP_PRIMITIVE_TYPES:dict[str, str] = {
        "INT": "int",
        "FLOAT": "float",
        "BOOL": "bool",
        "STRING": "string",
        "VAR": "var"
    }

    MAP_PRIMITIVE_VALUES:dict[str, str] = {
        "NONE": "none",
        "TRUE": "true",
        "FALSE": "false"
    }

    MAPPING:ChainMap[str, str] = ChainMap(
        MAP_KEYWORDS,
        MAP_FLAGS,
        MAP_PRIMITIVE_TYPES,
        MAP_PRIMITIVE_VALUES
    )


    # Stripping
    #---------------------------------------------

    @staticmethod
    def whitespace(line:str) -> str:
        """
        Replaces all consecutive whitespace in the input string with a single space.
        Returns the normalized string.
        """
        return re.sub(r'\s+', ' ', line).strip()


    @staticmethod
    def strip_comments(line:str) -> str:
        """
        Strips this line of any Papyrus comments.

        Example: (;...), (;/.../;)
        >>> strip_comments('Function Foo(int x = 5) ; This is a comment')
        >>> strip_comments('Function Foo(int ;/This is a comment/; x = 5)')
        """
        # Remove single line block comments: ;/.../;
        line = re.sub(r';/.*?/;', '', line)

        # Remove line comments: ;...
        line = re.split(r';', line, maxsplit=1)[0]

        # Remove whitespace from the end of the line
        return line.rstrip()


    # Papyrus
    #---------------------------------------------

    @staticmethod
    def symbol(token:str) -> str:
        """Normalize Papyrus keywords, flags, and other symbols."""
        if token: return Normalize.MAPPING.get(token.upper(), token)
        else: return token


    @staticmethod
    def flag(token:str) -> str:
        if token: return Normalize.MAP_FLAGS.get(token.upper(), token)
        else: return token


    @staticmethod
    def primitive_type(token:str) -> str:
        if token: return Normalize.MAP_PRIMITIVE_TYPES.get(token.upper(), token)
        else: return token


    @staticmethod
    def primitive_value(token:str) -> str:
        """Normalize primitive default values (none, true, false) (not numbers or strings)."""
        if token: return Normalize.MAP_PRIMITIVE_VALUES.get(token.upper(), token)
        else: return token


    # Script
    #---------------------------------------------

    @staticmethod
    def definition(line:str) -> str:
        """Normalizes the given Papyrus definition line."""
        line = Normalize.strip_comments(line)
        line = Normalize.whitespace(line)
        tokens:list[str] = line.split()
        return " ".join(Normalize.symbol(token) for token in tokens)


    @staticmethod
    def script_flags(flags:list[str]) -> list[str]:
        """Normalizes the given Papyrus flag symbol names."""
        return [Normalize.symbol(flag) for flag in flags]


    # TODO: REVIEW: This is under review.
    @staticmethod
    def script_type(token:str) -> str:
        """
        Papyrus primitive types are lowercase, object types are PascalCase.
        Handles arrays and 'none'.
        """
        if not token: return ""

        # Strip whitespace
        token = token.strip()

        # Strip array notation
        is_array:bool = False
        if token.endswith("[]"):
            is_array = True
            token = token[:-2]

        # Normalize the type
        if token.upper() in Normalize.MAP_PRIMITIVE_TYPES:
            token = Normalize.primitive_type(token)
        else:
            token = token[:1].upper() + token[1:]

        # Return the normalized type with array notation if applicable
        if is_array: return f"{token}[]"
        else: return token


    # TODO: REVIEW: This is under review. A new strategy is needed for member name normalization.
    @staticmethod
    def member_name_upper(name:str) -> str:
        return name[:1].upper() + name[1:]


    # TODO: REVIEW: This is under review.
    @staticmethod
    def member_name(name:str) -> str:
        return name
