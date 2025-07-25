"""
Generates MediaWiki pages for Papyrus members.
    Module: `app.wiki.page.member`
"""
from scribe import wiki
from scribe.app.context import AppContext
from scribe.papyrus.project import PapyrusProject
from scribe.papyrus.code import Script
from scribe.papyrus.code import Member
from scribe.papyrus.code import Function
from scribe.papyrus.code import Event
from scribe.papyrus.code import Variable
from scribe.papyrus.code import Property


def content(context:AppContext, project:PapyrusProject, script:Script, member:Member) -> list[str]:
    content:list[str] = []
    game_version:str = ""
    source_file_path:str = script.header.name.file_path() + ".psc"

    # Member Summary Template
    content.append(wiki.template.generator.script_member_summary(script, member, game_version))
    content.append("\n\n")

    # Member Documentation
    content.append("== Documentation ==\n")
    if not member.documentation:
        content.append(f"No documentation comments were provided for this member.\n")
        content.append("\n\n")
    else:
        content.append(f"The <code>{source_file_path}</code> source file documentation comments for this script.\n\n")
        content.append("<source>\n")
        content.append(f"{member.documentation}\n")
        content.append("</source>\n")
        content.append("\n\n")

    # Member Auto Value
    if isinstance(member, Property) or isinstance(member, Variable):
        content.append("== Field Initializer ==\n")
        if not member.value:
            content.append(f"This {str.lower(member.kind)} member has no field initialized value.\n\n")
        else:
            content.append("* " + member.value)
            content.append("\n")

    # Member Parameters
    if isinstance(member, Function) or isinstance(member, Event):
        content.append("== Parameters ==\n")
        if not member.parameters:
            content.append(f"This {str.lower(member.kind)} member has no parameters.\n\n")
        else:
            content.append("The parameters that belong to this script.\n\n")
            items = wiki.data.script.variable_to_string_list(member.parameters)
            for item in items:
                content.append(f"* {item}\n")

    # Page Categories
    # TODO: Should this be a different category for members?
    content.append("\n\n")
    content.append("[[Category:Starfield_Mod-Papyrus]]\n")
    return content


# Write
#---------------------------------------------

def write(context:AppContext, project:PapyrusProject, script:Script, member:Member, output_file_path:str) -> None:
    lines:list[str] = content(context, project, script, member)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
