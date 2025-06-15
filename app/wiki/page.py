from app import wiki, papyrus
from app.papyrus.code import Script


# Writer
#---------------------------------------------

def write(script:Script, output_file_path:str):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    game_version = ""

    # Write the wiki page text content
    with open(output_file_path, "w", encoding="utf-8") as file:
        # Script Summary Template
        file.write(wiki.template.script_object_summary(script, game_version))
        file.write("\n\n")

        # Script Definition
        file.write("== Definition ==\n")
        file.write(f"The <code>{script.header.name.file_path()}.psc</code> source file header definition for this script.\n\n")
        file.write("<source lang=\"papyrus\">\n")
        file.write(f"{script.header.definition}\n")
        file.write("</source>\n")
        file.write("\n\n")

        # Script Documentation
        file.write("== Documentation ==\n")
        if not script.header.documentation:
            file.write(f"No documentation comments were provided in the <code>{script.header.name.file_path()}.psc</code> source file.\n")
            file.write("\n\n")
        else:
            file.write(f"The <code>{script.header.name.file_path()}.psc</code> source file documentation comments for this script.\n\n")
            file.write("<source>\n")
            file.write(f"{script.header.documentation}\n")
            file.write("</source>\n")
            file.write("\n\n")

        # Script Members
        file.write("== Members ==\n")
        if not script.members:
            file.write(f"No members were defined in the <code>{script.header.name.file_path()}.psc</code> source file.\n\n")
        else:
            file.write("The members that belong to this script.\n\n")
            for member in script.members:
                file.write(wiki.template.script_object_member_summary(script, member, game_version))
                file.write("\n")

        # Page Categories
        file.write("\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")


def parse_write(script_file_path:str, output_file_path:str):
    script:Script = papyrus.parser.parse(script_file_path)
    write(script, output_file_path)
