import re
from typing import ChainMap, Dict

# Canonical Name Mappings
#---------------------------------------------

MAP_KEYWORDS:Dict[str, str] = {
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

MAP_FLAGS:Dict[str, str] = {
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

MAP_PRIMITIVE_TYPES:Dict[str, str] = {
    "INT": "int",
    "FLOAT": "float",
    "BOOL": "bool",
    "STRING": "string",
    "VAR": "var"
}

MAP_PRIMITIVE_VALUES:Dict[str, str] = {
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

def whitespace(line:str) -> str:
    """
    Replaces all consecutive whitespace in the input string with a single space.
    Returns the normalized string.
    """
    return re.sub(r'\s+', ' ', line).strip()


def strip_comments(line:str) -> str:
    """
    Strips this line of any Papyrus comments.

    Example: (;...), (;/.../;)
    >>> strip_comments('Function Foo(int x = 5) ; This is a comment')
    >>> strip_comments('Function Foo(int ;/This is a comment/; x = 5)')
    """
    # Remove block comments: ;/.../;
    line = re.sub(r';/.*?/;', '', line)

    # Remove line comments: ;...
    line = re.split(r';', line, maxsplit=1)[0]

    # Remove whitespace from the end of the line
    return line.rstrip()


# Papyrus
#---------------------------------------------

def symbol(token:str) -> str:
    """Normalize Papyrus keywords, flags, and other symbols."""
    if token: return MAPPING.get(token.upper(), token)
    else: return token


def flag(token:str) -> str:
    if token: return MAP_FLAGS.get(token.upper(), token)
    else: return token


def primitive_type(token:str) -> str:
    if token: return MAP_PRIMITIVE_TYPES.get(token.upper(), token)
    else: return token


def primitive_value(token:str) -> str:
    """Normalize primitive default values (none, true, false) (not numbers or strings)."""
    if token: return MAP_PRIMITIVE_VALUES.get(token.upper(), token)
    else: return token


# Script
#---------------------------------------------

def script_definition(line:str) -> str:
    """Normalizes the given Papyrus header."""
    tokens:list[str] = line.strip().split()
    return " ".join(symbol(token) for token in tokens)


def script_flags(flags:list[str]) -> list[str]:
    """Normalizes the given Papyrus flag symbol names."""
    return [symbol(flag) for flag in flags]


# TODO: REVIEW: This is under review.
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
    if token.upper() in MAP_PRIMITIVE_TYPES:
        token = primitive_type(token)
    else:
        token = token[:1].upper() + token[1:]

    # Return the normalized type with array notation if applicable
    if is_array: return f"{token}[]"
    else: return token


# TODO: REVIEW: This is under review. A new strategy is needed for member name normalization.
def member_name_upper(name:str) -> str:
    return name[:1].upper() + name[1:]


# TODO: REVIEW: This is under review.
def member_name(name:str) -> str:
    return name
