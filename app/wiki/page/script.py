"""
Generates MediaWiki pages for Papyrus scripts.
    Module: `app.wiki.page.script`
"""
from collections import defaultdict
from typing import DefaultDict
from app import wiki
from app.context import AppContext
from app.papyrus.project import PapyrusProject
from app.papyrus.code import Script
from app.papyrus.code import Member


def content(context:AppContext, project:PapyrusProject, script:Script) -> list[str]:
    content:list[str] = []
    game_version:str = ""
    source_file_path:str = script.header.name.file_path() + ".psc"

    # Script Summary Template
    content.append(wiki.template.generator.script_object_summary(context, project, script, game_version))
    content.append("\n\n")

    # Script Definition
    content.append("== Definition ==\n")
    content.append(f"The <code>{source_file_path}</code> source file header definition for this script.\n\n")
    content.append("<source lang=\"papyrus\">\n")
    content.append(f"{script.header.definition}\n")
    content.append("</source>\n")
    content.append("\n\n")

    # Script Documentation
    content.append("== Documentation ==\n")
    if not script.header.documentation:
        content.append(f"No documentation comments were provided in the <code>{source_file_path}</code> source file.\n")
        content.append("\n\n")
    else:
        content.append(f"The <code>{source_file_path}</code> source file documentation comments for this script.\n\n")
        content.append("<source>\n")
        content.append(f"{script.header.documentation}\n")
        content.append("</source>\n")
        content.append("\n\n")

    # Script Members
    content.append("== Member ==\n")
    if not script.members:
        content.append(f"No members were defined in the <code>{source_file_path}</code> source file.\n\n")
    else:
        content.append("The members that belong to this script, grouped by kind.\n\n")

        # Group members by kind
        members_by_kind:DefaultDict[str, list[Member]] = defaultdict(list)
        for member_key in script.members:
            member:Member = script.members[member_key]
            members_by_kind[member.kind].append(member)

        # Write each section of members by kind
        for kind, members in members_by_kind.items():
            content.append(f"=== {kind} ===\n")
            for member_key in members:
                content.append(wiki.template.generator.script_object_member_summary(script, member_key, game_version))
                content.append("\n")

    # Page Categories
    content.append("\n")
    content.append("[[Category:Starfield_Mod-Papyrus]]\n")
    return content


# Write
#---------------------------------------------

def write(context:AppContext, project:PapyrusProject, script:Script, output_file_path:str) -> None:
    """Generates a MediaWiki page for a given Papyrus script source file."""
    lines:list[str] = content(context, project, script)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
