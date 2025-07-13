"""
Provides wiki template generation features.
    Module: `app.wiki.template.generator`
"""
from app import wiki
from app.context import AppContext
from app.papyrus import inheritance
from app.papyrus.project import PapyrusProject
from app.papyrus.code import Script
from app.papyrus.code import Member
from app.wiki import template


# Script Object
#---------------------------------------------

def script_object_summary(context:AppContext, project:PapyrusProject, script:Script, game_version:str) -> str:
    """
    Gets the 'Script_Object_Summary' wiki template as a string.

    See: https://starfieldwiki.net/wiki/Template:Script_Object_Summary
    """
    script_title:str = str(script.header.name)
    script_name:str = wiki.formatter.link_script_object(str(script.header.name))
    inheritance_chain:list[Script] = inheritance.get_chain(context.papyrus, project, script)
    script_extends:str = wiki.data.inheritance.format_inheritance_chain(inheritance_chain)
    script_flags:str = wiki.formatter.to_list_csv(script.header.flags)
    #---------------------------------------------
    template_text:str = ""
    template_text += "{{Script_Object_Summary\n"

    if script_title:
        template_text += f"| title = {script_title}\n"

    if script_name:
        template_text += f"| name = {script_name}\n"

    if script_extends:
        template_text += f"| extends = {script_extends}\n"

    if script_flags:
        template_text += f"| flags = {script_flags}\n"

    if game_version:
        template_text += f"| game_version = {game_version}\n"

    template_text += "}}\n"
    return template_text


def script_object_member_summary(script:Script, member:Member, game_version:str) -> str:
    """
    Gets the 'Script_Object_Member_Summary' wiki template as a string.

    See: https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
    """
    script_name:str = wiki.formatter.link_script_object(str(script.header.name))
    member_title:str = member.name
    member_name:str = wiki.formatter.link_script_member(str(script.header.name), member.name)
    member_kind:str = member.kind
    member_returns:str = template.data.get_member_type_string(member)
    member_flags_string:str = " ".join(member.flags)
    member_parameters_string:str = template.data.get_member_parameters_string(member)
    member_documentation:str = member.documentation
    #---------------------------------------------
    template_text:str = ""
    template_text += "{{Script_Object_Member_Summary\n"

    if member_title:
        template_text += f"| title = {member_title}\n"

    if script_name:
        template_text += f"| script = {script_name}\n"

    if member_name:
        template_text += f"| name = {member_name}\n"

    if member_kind:
        template_text += f"| kind = {member_kind}\n"

    if member_flags_string:
        template_text += f"| flags = {member_flags_string}\n"

    if member_returns:
        template_text += f"| returns = {member_returns}\n"

    if member_parameters_string:
        template_text += f"| parameters = {member_parameters_string}\n"

    if member_documentation:
        template_text += f"| documentation = {member_documentation}\n"

    if game_version:
        template_text += f"| game_version = {game_version}\n"

    template_text += "}}\n"
    return template_text


# Not implemented yet, for standalone member pages
def script_member_summary(script:Script, member:Member, game_version:str) -> str:
    """
    Gets the 'Script_Member_Summary' wiki template as a string.

    See: https://starfieldwiki.net/wiki/Template:Script_Member_Summary
    """
    script_name:str = wiki.formatter.link_script_object(str(script.header.name))
    member_title:str = member.name
    member_name:str = wiki.formatter.link_script_member(str(script.header.name), member.name)
    member_kind:str = member.kind
    member_returns:str = template.data.get_member_type_string(member)
    member_flags_string:str = " ".join(member.flags)
    member_parameters_string:str = template.data.get_member_parameters_string(member)
    member_documentation:str = member.documentation
    #---------------------------------------------
    template_text:str = ""
    template_text += "{{Script_Member_Summary\n"

    if member_title:
        template_text += f"| title = {member_title}\n"

    if script_name:
        template_text += f"| script = {script_name}\n"

    if member_name:
        template_text += f"| name = {member_name}\n"

    if member_kind:
        template_text += f"| kind = {member_kind}\n"

    if member_flags_string:
        template_text += f"| flags = {member_flags_string}\n"

    if member_returns:
        template_text += f"| returns = {member_returns}\n"

    if member_parameters_string:
        template_text += f"| parameters = {member_parameters_string}\n"

    if member_documentation:
        template_text += f"| documentation = {member_documentation}\n"

    if game_version:
        template_text += f"| game_version = {game_version}\n"

    template_text += "}}\n"
    return template_text
