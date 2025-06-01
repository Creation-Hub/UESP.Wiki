import papyrus.parser
import wiki.template

# Writer
#---------------------------------------------

def write(script_path, output_path):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    (
        header,
        members
    ) = papyrus.parser.parse(script_path)

    script_header = header["header"]
    script_name = header["name"]
    script_extends = header["extends"]
    script_doc = header["doc"]

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
            game_version = ""
            file.write(
                wiki.template.script_object_member_summary
                (
                    script_name,
                    member,
                    game_version
                )
            )
            file.write("\n")

        # Page Categories
        file.write("\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")
