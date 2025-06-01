import re

# Normalize
#---------------------------------------------

def script_keyword(word: str) -> str:
    """Normalize Papyrus keywords and flags to CamelCase."""
    mapping = {
        # Keywords
        "scriptname": "ScriptName",
        "extends": "Extends",
        "function": "Function",
        "event": "Event",
        "property": "Property",
        "struct": "Struct",
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
        "betaonly": "BetaOnly"
    }
    return mapping.get(word.lower(), word)


def script_type(type_str: str) -> str:
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
    primitive_types = {"int", "float", "bool", "string", "var", "none"}
    if t.lower() in primitive_types:
        base = t.lower()
    else:
        base = t[:1].upper() + t[1:]
    return f"{base}[]" if is_array else base


def member_name(name: str) -> str:
    """Ensure member names are CamelCase."""
    if not name:
        return ""
    return name[0].upper() + name[1:]


def script_header(header_line: str) -> str:
    """Ensure Papyrus header keywords and flags are CamelCase."""
    tokens = header_line.strip().split()
    return " ".join(script_keyword(token) for token in tokens)


def script_flags(flag_tokens: list[str]) -> list[str]:
    """Normalize member flags to CamelCase."""
    return [script_keyword(f) for f in flag_tokens]


def default_value(default_val: str) -> str:
    """Normalize primitive default values (none, true, false, numbers)."""
    if not default_val:
        return ""
    val = default_val.strip()
    if val.startswith("="):
        val = val[1:].strip()
    primitive_values = {"none", "true", "false"}
    if val.lower() in primitive_values:
        return "= " + val.lower()
    try:
        float(val)
        return "= " + val
    except ValueError:
        pass
    return "= " + val


def strip_comments(line: str) -> str:
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
