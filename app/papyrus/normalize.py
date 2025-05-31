import re

# Normalize
#---------------------------------------------

def script_keyword(word):
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


def script_type(type_str):
    """Papyrus primitive types are lowercase, object types are CamelCase. Handles arrays and 'none'."""
    if not type_str:
        return ""
    t = type_str.strip()
    is_array = False
    if t.endswith("[]"):
        is_array = True
        t = t[:-2]
    primitives = {"int", "float", "bool", "string", "var", "none"}
    if t.lower() in primitives:
        base = t.lower()
    else:
        base = t[:1].upper() + t[1:]
    return f"{base}[]" if is_array else base


def member_name(name):
    """Ensure member names are CamelCase."""
    if not name:
        return ""
    return name[0].upper() + name[1:]


def script_header(header_line):
    """Ensure Papyrus header keywords and flags are CamelCase."""
    tokens = header_line.strip().split()
    return " ".join(script_keyword(token) for token in tokens)


def script_flags(flag_tokens):
    """Normalize member flags to CamelCase."""
    return [script_keyword(f) for f in flag_tokens]


def default_value(default_val):
    """Normalize primitive default values (none, true, false, numbers)."""
    if not default_val:
        return ""
    val = default_val.strip()
    if val.startswith("="):
        val = val[1:].strip()
    primitives = {"none", "true", "false"}
    if val.lower() in primitives:
        return "= " + val.lower()
    try:
        float(val)
        return "= " + val
    except ValueError:
        pass
    return "= " + val


def strip_comments(line):
    """
    Strips this line of any Papyrus comments. ex (;), (;/.../;)
    Only removes comments, not string literals.
    """
    # Remove block comments: ;/ ... /;
    line = re.sub(r';/.*?/;', '', line)
    # Remove line comments: ; ...
    line = re.split(r';', line, maxsplit=1)[0]
    return line.rstrip()
