import papyrus.normalize
import wiki
import app.wiki.style

# Members: Bulleted List
#---------------------------------------------

# Unused
def wiki_script_member(script_name, member):
    """
    Generate a MediaWiki formatted string for a script member.
    Returns a list of lines that can be written to a wiki page.

    Example:
        for line in wiki_script_member(script_name, member):
            f.write(f"{line}\n")
    """
    kind = member["kind"]
    lines = []

    if kind == "function":
        link = wiki.style.script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        param_str = ", ".join(member["params"])
        rtype = papyrus.normalize.script_type(member["rtype"]) if member.get("rtype") else ""
        if rtype:
            lines.append(f"* {rtype} {papyrus.normalize.symbol('function')} {link}({param_str}){flag_str}")
        else:
            lines.append(f"* {papyrus.normalize.symbol('function')} {link}({param_str}){flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "event":
        link = wiki.style.script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        param_str = ", ".join(member["params"])
        lines.append(f"* {papyrus.normalize.symbol('event')} {link}({param_str}){flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "property":
        link = wiki.style.script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        lines.append(f"* {member['type']} {papyrus.normalize.symbol('property')} {link}{flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "struct":
        link = wiki.style.script_member(script_name, member["name"])
        lines.append(f"* {papyrus.normalize.symbol('struct')} {link}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    return lines


# UNUSED: This function is not used in the current codebase.
def extract_header_extends(header_line:str) -> str:
    """
    Extracts the Extends value from the script header.
    Returns:
      - The script name after 'Extends' if present (may be namespaced).
      - 'Nothing' if this is ScriptObject itself.
      - 'ScriptObject' if no Extends is present.
    """
    clean_line = papyrus.normalize.strip_comments(header_line)
    tokens = clean_line.strip().split()
    script_name = None
    extends_name = None

    for i, token in enumerate(tokens):
        if token.lower() == "scriptname" and i + 1 < len(tokens):
            script_name = tokens[i + 1]
        if token.lower() == "extends" and i + 1 < len(tokens):
            extends_name = tokens[i + 1]

    if extends_name:
        return extends_name
    elif script_name and script_name.endswith("ScriptObject"):
        return "Nothing"
    else:
        return "ScriptObject"
