import re

# Normalize
#---------------------------------------------

def whitespace(line:str) -> str:
    """
    Replaces all consecutive whitespace in the input string with a single space.
    Returns the normalized string.
    """
    return re.sub(r'\s+', ' ', line).strip()


# Papyrus
#---------------------------------------------

def symbol(token:str) -> str:
    """Normalize Papyrus keywords, flags, and other symbols."""
    mapping = {
        # Keywords
        "scriptname": "ScriptName",
        "extends": "Extends",
        "state": "State",
        "function": "Function",
        "event": "Event",
        "property": "Property",
        "struct": "Struct",
        "guard": "Guard",
        # Flags
        "native": "Native",
        "const": "Const",
        "hidden": "Hidden",
        "conditional": "Conditional",
        "default": "Default",
        "selfonly": "SelfOnly",
        "private": "Private",
        "protected": "Protected",
        "global": "Global",
        "auto": "Auto",
        "mandatory": "Mandatory",
        "readonly": "ReadOnly",
        "debugonly": "DebugOnly",
        "betaonly": "BetaOnly",
        # Primitive Types
        "int": "int",
        "float": "float",
        "bool": "bool",
        "string": "string",
        "var": "var",
        # Primitive Values
        "none": "none",
        "true": "true",
        "false": "false"
    }
    return mapping.get(token.lower(), token)


# Script
#---------------------------------------------

def script_definition(line:str) -> str:
    """Normalizes the given Papyrus header."""
    tokens = line.strip().split()
    return " ".join(symbol(token) for token in tokens)


def script_flags(flags:list[str]) -> list[str]:
    """Normalizes the given Papyrus flag symbol names."""
    return [symbol(flag) for flag in flags]


def script_type(type_str:str) -> str:
    """
    Papyrus primitive types are lowercase, object types are CamelCase.
    Handles arrays and 'none'.
    """
    if not type_str:
        return ""
    # Strip whitespace
    t = type_str.strip()
    # Check for array notation
    is_array = False
    if t.endswith("[]"):
        is_array = True
        t = t[:-2]
    # Normalize primitive types
    #TODO: Use symbol() to normalize primitive types?
    primitive_types = {"int", "float", "bool", "string", "var", "none"}
    if t.lower() in primitive_types:
        base = t.lower()
    else:
        base = t[:1].upper() + t[1:]
    return f"{base}[]" if is_array else base


def member_name(name:str) -> str:
    """Ensure member names are CamelCase. Set first letter to uppercase."""
    if not name:
        return ""
    return name[0].upper() + name[1:]


def default_value(default_val:str) -> str:
    """Normalize primitive default values (none, true, false, numbers)."""
    if not default_val:
        return ""
    val = default_val.strip()
    if val.startswith("="):
        val = val[1:].strip()
    #TODO: Use symbol() to normalize primitive values?
    primitive_values = {"none", "true", "false"}
    if val.lower() in primitive_values:
        return "= " + val.lower()
    try:
        float(val)
        return "= " + val
    except ValueError:
        pass
    return "= " + val


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
    return line.rstrip()
