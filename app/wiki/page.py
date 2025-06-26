from app import wiki
from app.context import AppContext
from app.project import PapyrusProject
from app.papyrus.code import Script
from app.papyrus.code import Member
from app.papyrus.code import Function
from app.papyrus.code import Event
from app.papyrus.code import Variable
from app.papyrus.code import Property


# Writer: Script Object
#---------------------------------------------

def write_script(context:AppContext, project:PapyrusProject, script:Script, output_file_path:str):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    game_version = ""
    source_file_path:str = script.header.name.file_path() + ".psc"

    # Write the wiki page text content
    with open(output_file_path, "w", encoding="utf-8") as file:
        # Script Summary Template
        file.write(wiki.template.script_object_summary(context, project, script, game_version))
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
        file.write("== Member ==\n")
        if not script.members:
            file.write(f"No members were defined in the <code>{source_file_path}</code> source file.\n\n")
        else:
            file.write("The members that belong to this script, grouped by kind.\n\n")
            # Group members by kind
            from collections import defaultdict
            from typing import DefaultDict
            members_by_kind:DefaultDict[str, list[Member]] = defaultdict(list)
            for member in script.members:
                members_by_kind[member.kind].append(member)
            # Write each kind section
            for kind, members in members_by_kind.items():
                file.write(f"=== {kind} ===\n")
                for member in members:
                    file.write(wiki.template.script_object_member_summary(script, member, game_version))
                    file.write("\n")

        # Page Categories
        file.write("\n")
        file.write("[[Category:Starfield_Mod-Papyrus]]\n")


# Writer: Script Member
#---------------------------------------------

def write_member(context:AppContext, project:PapyrusProject, script:Script, member:Member, output_file_path:str):
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

        # Member Auto Value
        if isinstance(member, Property) or isinstance(member, Variable):
            file.write("== Field Initializer ==\n")
            if not member.value_auto:
                file.write(f"This {str.lower(member.kind)} member has no field initialized value.\n\n")
            else:
                file.write("* " + member.value_auto)
                file.write("\n")

        # Member Parameters
        if isinstance(member, Function) or isinstance(member, Event):
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
