import papyrus.normalize
import papyrus.parser
import wiki.link
import wiki.meta
import wiki.template

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


# Writer
#---------------------------------------------

def write(script_path, output_path):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    # Collect script information
    script_name, header_line, documentation, members = papyrus.parser.parse_script(script_path)
    extends_value = papyrus.parser.extract_script_extends(header_line)

    # Write the wiki page text content
    with open(output_path, "w", encoding="utf-8") as file:
        # Meta Information (Hidden)
        wiki.meta.write(file, script_path)
        file.write("\n\n")

        # Script Summary Template
        file.write(wiki.template.script_object_summary(script_name, script_name, extends_value))
        file.write("\n\n")

        # Script Definition
        file.write("== Definition ==\n")
        file.write(f"The <code>{script_name}.psc</code> source file header definition for this script.\n\n")
        file.write("<source lang=\"papyrus\">\n")
        file.write(f"{papyrus.normalize.strip_comments(header_line)}\n")
        file.write("</source>\n\n\n")

        # Script Documentation
        file.write("== Documentation ==\n")
        file.write(f"The <code>{script_name}.psc</code> source file documentation comments for this script.\n\n")
        file.write("<source>\n")
        file.write(f"{documentation}\n")
        file.write("</source>\n\n\n")

        # Script Members
        file.write("== Members ==\n")
        file.write("The members that belong to this script.\n\n")
        for member in members:
            title = member["name"]
            member_name = member["name"]
            member_kind = member["kind"]
            member_rtype = member.get("rtype", "")
            member_flags = member.get("flags", [])
            member_params = member.get("params", [])
            member_doc = member.get("doc", "")
            game_version = "v0.0.0+" # TODO: Perhaps this should NOT be included in generation.
            file.write(
                wiki.template.script_object_member_summary(
                    title,
                    script_name,
                    member_name,
                    papyrus.normalize.script_keyword(member_kind),
                    member_rtype,
                    " ".join(member_flags) if isinstance(member_flags, list) else member_flags,
                    ", ".join(member_params) if isinstance(member_params, list) else member_params,
                    member_doc,
                    game_version
                )
            )
            file.write("\n")

        # Page Categories
        file.write("\n\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")
