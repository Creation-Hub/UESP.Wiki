from app import wiki
from app.papyrus.code import Script, Member


def get_script_extends(script:Script) -> str:
    if script.header.name.value == "ScriptObject":
        return "Nothing"
    elif script.header.extends.value:
        return wiki.style.link_script_object(script.header.extends)
    else:
        return wiki.style.link_script_object("ScriptObject")


# Script Object
#---------------------------------------------

def script_object_summary(script:Script, game_version):
    """
    Return the 'Script_Object_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Object_Summary
    """
    script_title = script.header.name
    script_name = wiki.style.link_script_object(script.header.name)
    script_extends = get_script_extends(script)
    script_flags = wiki.style.to_list_csv(script.header.flags)

    template_text = ""
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


def script_object_member_summary(script:Script, member:Member, game_version):
    """
    Return the 'Script_Object_Member_Summary' wiki template as a string.
    See https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
    """
    script_name = wiki.style.link_script_object(script.header.name)
    member_title = member.name
    member_name = wiki.style.link_script_member(script.header.name, member.name)
    member_kind = member.kind
    member_returns = member.type
    member_flags_string = " ".join(member.flags) if isinstance(member.flags, list) else member.flags
    member_parameters_string = ", ".join(member.parameters) if isinstance(member.parameters, list) else member.parameters
    member_documentation = member.documentation

    template_text = ""
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


# Script Member
#---------------------------------------------

# Not implemented yet, for standalone member pages
def script_member_summary(member_title, script_name, member_name, member_kind, member_returns, member_flags, member_parameters, documentation, game_version):
    """
    Return the 'Script_Member_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Member_Summary
    """
    return (
        "{{Script_Member_Summary\n"
        f"| title = {member_title}\n"
        f"| script = {wiki.style.link_script_object(script_name)}\n"
        f"| name = {wiki.style.link_script_member(script_name, member_name)}\n"
        f"| kind = {member_kind}\n"
        f"| flags = {member_flags}\n"
        f"| returns = {member_returns}\n"
        f"| parameters = {member_parameters}\n"
        f"| documentation = {game_version}\n"
        f"| game_version = {documentation}\n"
        "}}\n"
    )
