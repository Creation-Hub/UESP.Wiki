from app import wiki
from app.papyrus.code import Member, Script

# Writer: Script Object
#---------------------------------------------

def write_script(script:Script, output_file_path:str):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    game_version = ""
    source_file_path:str = script.header.name.file_path() + ".psc"

    # Write the wiki page text content
    with open(output_file_path, "w", encoding="utf-8") as file:
        # Script Summary Template
        file.write(wiki.template.script_object_summary(script, game_version))
        file.write("\n\n")

        # Script Definition
        file.write("== Definition ==\n")
        file.write(f"The <code>{source_file_path}</code> source file header definition for this script.\n\n")
        file.write("<source lang=\"papyrus\">\n")
        file.write(f"{script.header.definition}\n")
        file.write("</source>\n")
        file.write("\n\n")

        # Script Documentation
        file.write("== Documentation ==\n")
        if not script.header.documentation:
            file.write(f"No documentation comments were provided in the <code>{source_file_path}</code> source file.\n")
            file.write("\n\n")
        else:
            file.write(f"The <code>{source_file_path}</code> source file documentation comments for this script.\n\n")
            file.write("<source>\n")
            file.write(f"{script.header.documentation}\n")
            file.write("</source>\n")
            file.write("\n\n")

        # Script Members
        file.write("== Members ==\n")
        if not script.members:
            file.write(f"No members were defined in the <code>{source_file_path}</code> source file.\n\n")
        else:
            file.write("The members that belong to this script.\n\n")
            for member in script.members:
                file.write(wiki.template.script_object_member_summary(script, member, game_version))
                file.write("\n")

        # Page Categories
        file.write("\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")


# Writer: Script Member
#---------------------------------------------

def write_member(script:Script, member:Member, output_file_path:str):
    game_version = ""
    source_file_path:str = script.header.name.file_path() + ".psc"

    # Write the wiki page text content
    with open(output_file_path, "w", encoding="utf-8") as file:
        # Member Summary Template
        file.write(wiki.template.script_member_summary(script, member, game_version))
        file.write("\n\n")

        # Member Documentation
        file.write("== Documentation ==\n")
        if not member.documentation:
            file.write(f"No documentation comments were provided for this member.\n")
            file.write("\n\n")
        else:
            file.write(f"The <code>{source_file_path}</code> source file documentation comments for this script.\n\n")
            file.write("<source>\n")
            file.write(f"{member.documentation}\n")
            file.write("</source>\n")
            file.write("\n\n")

        # Member Parameters
        if member.kind == "Property":
            file.write("== Field Initializer ==\n")
            if not member.parameters:
                file.write(f"This {str.lower(member.kind)} member has no field initialized value.\n\n")
            else:
                file.write("* " + member.parameters[0])
                file.write("\n")
        else:
            file.write("== Parameters ==\n")
            if not member.parameters:
                file.write(f"This {str.lower(member.kind)} member has no parameters.\n\n")
            else:
                file.write("The parameters that belong to this script.\n\n")
                for parameter in member.parameters:
                    file.write("* " + parameter)
                    file.write("\n")

        # Page Categories
        # TODO: Should this be a different category for members?
        file.write("\n\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")
