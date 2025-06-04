import papyrus.parser
from papyrus.script import Script, Member
import wiki.template

# Writer
#---------------------------------------------

def write(script_path:str, output_path:str):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    script:Script = papyrus.parser.parse(script_path)
    game_version = ""

    # Write the wiki page text content
    with open(output_path, "w", encoding="utf-8") as file:
        # Script Summary Template
        file.write(wiki.template.script_object_summary(script, game_version))
        file.write("\n\n")

        # Script Definition
        file.write("== Definition ==\n")
        file.write(f"The <code>{script.header.name.path()}.psc</code> source file header definition for this script.\n\n")
        file.write("<source lang=\"papyrus\">\n")
        file.write(f"{script.header.definition}\n")
        file.write("</source>\n\n\n")

        # Script Documentation
        file.write("== Documentation ==\n")
        file.write(f"The <code>{script.header.name.path()}.psc</code> source file documentation comments for this script.\n\n")
        file.write("<source>\n")
        file.write(f"{script.header.documentation}\n")
        file.write("</source>\n\n\n")

        # Script Members
        file.write("== Members ==\n")
        file.write("The members that belong to this script.\n\n")
        for member in script.members:
            file.write(wiki.template.script_object_member_summary(script, member, game_version))
            file.write("\n")

        # Page Categories
        file.write("\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")
