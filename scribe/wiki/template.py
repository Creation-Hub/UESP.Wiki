"""
Provides wiki template generation features.
"""
from scribe.papyrus.context import PapyrusContext
from scribe.papyrus.inheritance import PapyrusInheritance
from scribe.papyrus.project import PapyrusProject
from scribe.papyrus.code import Script
from scribe.papyrus.code import Member
from scribe.wiki.article import Article
from scribe.wiki.data.inheritance import WikiDataInheritance
from scribe.wiki.formatter import WikiFormatter
from scribe.wiki.templates.data import TemplateData


class Template(Article):
    """
    Represents a MediaWiki template type.
    """
    def __init__(self) -> None:
        super().__init__()
        # TODO: Add a "help" page reference for templates.


    @staticmethod
    def create(file_path:str) -> 'Template':
        this:Template = Template()
        this.file_path = file_path
        return this


class Script_Object_Summary:
    @staticmethod
    def script_object_summary(papyrus:PapyrusContext, project:PapyrusProject, script:Script, game_version:str) -> str:
        """
        Gets the 'Script_Object_Summary' wiki template as a string.

        See: https://starfieldwiki.net/wiki/Template:Script_Object_Summary
        """
        script_title:str = str(script.header.name)
        script_name:str = WikiFormatter.link_script_object(str(script.header.name))
        inheritance_chain:list[Script] = PapyrusInheritance.get_chain(papyrus, project, script)
        script_extends:str = WikiDataInheritance.format_inheritance_chain(inheritance_chain)
        script_flags:str = WikiFormatter.to_list_csv(script.header.flags)
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


class Script_Object_Member_Summary:
    @staticmethod
    def script_object_member_summary(script:Script, member:Member, game_version:str) -> str:
        """
        Gets the 'Script_Object_Member_Summary' wiki template as a string.

        See: https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
        """
        script_name:str = WikiFormatter.link_script_object(str(script.header.name))
        member_title:str = member.name
        member_name:str = WikiFormatter.link_script_member(str(script.header.name), member.name)
        member_kind:str = member.kind
        member_returns:str = TemplateData.get_member_type_string(member)
        member_flags_string:str = " ".join(member.flags)
        member_parameters_string:str = TemplateData.get_member_parameters_string(member)
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


class Script_Member_Summary:
    # Not implemented yet, for standalone member pages
    @staticmethod
    def script_member_summary(script:Script, member:Member, game_version:str) -> str:
        """
        Gets the 'Script_Member_Summary' wiki template as a string.

        See: https://starfieldwiki.net/wiki/Template:Script_Member_Summary
        """
        script_name:str = WikiFormatter.link_script_object(str(script.header.name))
        member_title:str = member.name
        member_name:str = WikiFormatter.link_script_member(str(script.header.name), member.name)
        member_kind:str = member.kind
        member_returns:str = TemplateData.get_member_type_string(member)
        member_flags_string:str = " ".join(member.flags)
        member_parameters_string:str = TemplateData.get_member_parameters_string(member)
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
