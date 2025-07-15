from app import wiki
from app.context import AppContext
from app.papyrus.project import PapyrusProject
from app.papyrus.code import Script
from app.papyrus import inheritance


def summary(context:AppContext, project:PapyrusProject, script:Script) -> list[str]:
    script_title:str = str(script.header.name)
    script_name:str = wiki.formatter.link_script_object(str(script.header.name))
    inheritance_chain:list[Script] = inheritance.get_chain(context.papyrus, project, script)
    script_extends:str = wiki.data.inheritance.format_inheritance_chain(inheritance_chain)
    script_flags:str = wiki.formatter.to_list_csv(script.header.flags)
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
