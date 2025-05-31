import papyrus.normalize
import wiki.link
import wiki.meta

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
        link = wiki.link.script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        param_str = ", ".join(member["params"])
        rtype = papyrus.normalize.script_type(member["rtype"]) if member.get("rtype") else ""
        if rtype:
            lines.append(f"* {rtype} {papyrus.normalize.script_keyword('function')} {link}({param_str}){flag_str}")
        else:
            lines.append(f"* {papyrus.normalize.script_keyword('function')} {link}({param_str}){flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "event":
        link = wiki.link.script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        param_str = ", ".join(member["params"])
        lines.append(f"* {papyrus.normalize.script_keyword('event')} {link}({param_str}){flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "property":
        link = wiki.link.script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        lines.append(f"* {member['type']} {papyrus.normalize.script_keyword('property')} {link}{flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "struct":
        link = wiki.link.script_member(script_name, member["name"])
        lines.append(f"* {papyrus.normalize.script_keyword('struct')} {link}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    return lines
