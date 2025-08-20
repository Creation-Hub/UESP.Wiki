from papyrus.client import PapyrusClient
from papyrus.inheritance import PapyrusInheritance
from papyrus.project import PapyrusProject
from papyrus.code import Script
from papyrus.code import Member
from wiki.data.formatting import Text
from scribe.composer.wiki import Wiki
from .scripts_inheritance import WikiDataInheritance
from .templates_data import TemplateData


class Script_Object_Summary:

    # Creates the template definition.
    @staticmethod
    def _create_content(papyrus:PapyrusClient, project:PapyrusProject, script:Script) -> list[str]:
        script_title:str = str(script.header.name)
        script_name:str = Wiki.link_script_object(str(script.header.name))
        inheritance_chain:list[Script] = PapyrusInheritance.get_chain(papyrus, project, script)
        script_extends:str = WikiDataInheritance.format_inheritance_chain(inheritance_chain)
        script_flags:str = Text.list_csv(script.header.flags)
        editor:str = ""
        base:str = ""
        reference:str = ""
        #---------------------------------------------
        content:list[str] = []
        content.append("<cleantable>\n")
        content.append("{| class=\"wikitable infobox\"\n")

        # Title
        content.append(f"!colspan=2| {script_title}\n")

        # Name
        content.append("|-\n")
        content.append("![[SFM:Object_Scripts|Script]]\n")
        content.append(f"|{script_name}\n")

        # Extends
        content.append("|-\n")
        content.append("!Extends\n")
        content.append(f"|{script_extends}\n")

        # Flags
        content.append("|-\n")
        content.append("!Flags\n")
        content.append(f"|{script_flags}\n")

        # Editor
        content.append("|-\n")
        content.append("![[SFM:Form_Reference|Editor]]\n")
        content.append(f"|{editor}\n")

        # Base
        content.append("|-\n")
        content.append("!Base\n")
        content.append(f"|{base}\n")

        # Reference
        content.append("|-\n")
        content.append("![[SFM:Reference|Reference]]\n")
        content.append(f"|{reference}\n")

        # content.append("|\n")
        content.append("|}\n")
        content.append("</cleantable>\n")

        return content


    # Gets the template usage syntax.
    @staticmethod
    def template(papyrus:PapyrusClient, project:PapyrusProject, script:Script, game_version:str) -> str:
        """
        Gets the 'Script_Object_Summary' wiki template as a string.

        See: https://starfieldwiki.net/wiki/Template:Script_Object_Summary
        """
        script_title:str = str(script.header.name)
        script_name:str = Wiki.link_script_object(str(script.header.name))
        inheritance_chain:list[Script] = PapyrusInheritance.get_chain(papyrus, project, script)
        script_extends:str = WikiDataInheritance.format_inheritance_chain(inheritance_chain)
        script_flags:str = Text.list_csv(script.header.flags)
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
    def template(script:Script, member:Member, game_version:str) -> str:
        """
        Gets the 'Script_Object_Member_Summary' wiki template as a string.

        See: https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
        """
        script_name:str = Wiki.link_script_object(str(script.header.name))
        member_title:str = member.name
        member_name:str = Wiki.link_script_member(str(script.header.name), member.name)
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
    def template(script:Script, member:Member, game_version:str) -> str:
        """
        Gets the 'Script_Member_Summary' wiki template as a string.

        See: https://starfieldwiki.net/wiki/Template:Script_Member_Summary
        """
        script_name:str = Wiki.link_script_object(str(script.header.name))
        member_title:str = member.name
        member_name:str = Wiki.link_script_member(str(script.header.name), member.name)
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
