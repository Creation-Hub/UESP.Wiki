"""
Provides MediaWiki data transformations for Papyrus scripts.
"""
from scribe.papyrus.code import Script
from scribe.papyrus.code import Member
from scribe.papyrus.code import Method
from scribe.papyrus.code import Function
from scribe.papyrus.code import Property
from scribe.papyrus.code import Variable
from scribe.wiki.data.script import WikiDataScript
from scribe.wiki.formatter import WikiFormatter

class TemplateData:
    """
    Provides methods for generating wiki templates data.
    """

    # TODO: This is currently unused.
    @staticmethod
    def get_script_extends_link(script:Script) -> str:
        """
        Gets the MediaWiki link to the script extends for the script index page.
        """
        if script.header.name.key == "ScriptObject":
            return "Nothing"
        elif script.header.extends.key:
            return WikiFormatter.link_script_object(str(script.header.extends))
        else:
            return WikiFormatter.link_script_object("ScriptObject")


    @staticmethod
    def get_member_type_string(member:Member) -> str:
        """
        Gets the returns string for a member template.
        Templates need to have minimal returns that accommodate several member types.
        """
        if  isinstance(member, Variable) \
            or isinstance(member, Property) \
            or isinstance(member, Function):
            return str(member.type)
        else:
            return ""


    @staticmethod
    def get_member_parameters_string(member:Member) -> str:
        """
        Gets the parameters string for a member template.
        Templates need to have minimal parameters that accommodate several member types.
        """
        # Process types from the most specialized to the least.
        if isinstance(member, Method):
            return ", ".join(WikiDataScript.variable_to_string_list(member.parameters))
        elif isinstance(member, Variable):
            return member.value
        else:
            return ""
