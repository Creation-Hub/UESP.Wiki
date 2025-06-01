import papyrus.normalize
import papyrus.parser
import wiki.template

# Writer
#---------------------------------------------

def write(script_path, output_path):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    (# Collect script information
        script_header,
        script_name,
        script_extends,
        script_doc,
        members
    ) = papyrus.parser.parse_script(script_path)

    # Write the wiki page text content
    with open(output_path, "w", encoding="utf-8") as file:
        # Script Summary Template
        file.write(wiki.template.script_object_summary(script_name, script_name, script_extends))
        file.write("\n\n")

        # Script Definition
        file.write("== Definition ==\n")
        file.write(f"The <code>{script_name}.psc</code> source file header definition for this script.\n\n")
        file.write("<source lang=\"papyrus\">\n")
        file.write(f"{script_header}\n")
        file.write("</source>\n\n\n")

        # Script Documentation
        file.write("== Documentation ==\n")
        file.write(f"The <code>{script_name}.psc</code> source file documentation comments for this script.\n\n")
        file.write("<source>\n")
        file.write(f"{script_doc}\n")
        file.write("</source>\n\n\n")

        # Script Members
        file.write("== Members ==\n")
        file.write("The members that belong to this script.\n\n")
        for member in members:
            title = member["name"]
            member_name = member["name"]
            member_kind = member["kind"]
            member_kind = papyrus.normalize.script_keyword(member_kind) # TODO: Refactor this to occur earlier in the parser.
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
                    member_kind,
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
