"""
Generates a MediaWiki page that summarizes information about all Papyrus projects.
    Module: `app.wiki.page.index`
"""
from collections import Counter
from collections.abc import ItemsView
import logging
from app import wiki
from app.context import AppContext
from app.papyrus.code import Member
from app.papyrus.project import PapyrusProject


# Information
#---------------------------------------------

def statistics_project(project:PapyrusProject) -> \
    tuple[int, int, Counter[str], Counter[str]]:
    # Initialize count trackers
    script_extends_counter:Counter[str] = Counter()
    script_member_kind_counter:Counter[str] = Counter()

    # Iterate through each script to count each use of extends
    for script in project.scripts:
        script_name:str = script.header.extends.key
        if not script_name: script_name = "ScriptObject"
        script_extends_counter[script_name] += 1

        # Iterate through each member in the script to count their kinds
        for member_key in script.members:
            member:Member = script.members[member_key]
            script_member_kind_counter[member.kind] += 1

    return (
        len(project.imports),
        len(project.scripts),
        script_extends_counter,
        script_member_kind_counter
    )


# MediaWiki
#---------------------------------------------

def wiki_list_project_imports(project:PapyrusProject) -> str:
    return ", ".join(project.imports) if project.imports else "Nothing"


def wiki_list_member_kinds(script_member_kind_counter:Counter[str]) -> str:
    kinds:ItemsView[str, int] = script_member_kind_counter.items()
    if not kinds:
        return "There are no members defined in this project."
    entries:list[str] = []
    for kind, count in kinds:
        entries.append(f"* {kind} was used {count} times.")
    return "\n".join(entries)


def wiki_list_extends_most_common(script_extends_counter:Counter[str]) -> str:
    common_parent_names:list[tuple[str, int]] = script_extends_counter.most_common(3)
    if not common_parent_names:
        return "There are no common scripts in this project."
    entries:list[str] = []
    for script_name, count in common_parent_names:
        entries.append(f"* The {wiki.formatter.link_script_object(script_name)} script was extended {count} times.")
    return "\n".join(entries)


def wiki_list_script_names(project:PapyrusProject) -> str:
    if not project.scripts:
        return "There are no scripts defined in this project."
    entries:list[str] = []
    for script in project.scripts:
        entries.append(f"* {wiki.formatter.link_script_object(str(script.header.name))}")
    return "\n".join(entries)


# Write
#---------------------------------------------

def write_section(content:list[str], project:PapyrusProject) -> None:
    ( # Collect information for this project
        project_imports_count,
        project_scripts_count,
        script_extends_counter,
        script_member_kind_counter
    ) = statistics_project(project)

    # Add project summary information
    content.append(f"== {project.identifier} ==\n")
    content.append(f"* Imports: {project_imports_count} ({wiki_list_project_imports(project)})\n")
    content.append(f"* Scripts: {project_scripts_count}\n")
    content.append("\n")

    # Add script member statistics section
    content.append("==== Member Statistics ====\n")
    if project_scripts_count:
        content.append(f"This project overall contains {script_member_kind_counter.total()} total members spread over {project_scripts_count} scripts.\n")
        content.append(wiki_list_member_kinds(script_member_kind_counter)+"\n")
    else:
        content.append("There are no scripts defined in this project, so no member statistics can be provided.\n")
    content.append("\n")

    # Add script inheritance statistics section
    content.append("==== Inheritance Statistics ====\n")
    if project_scripts_count:
        content.append(f"The most common extended parent scripts:\n")
        content.append(wiki_list_extends_most_common(script_extends_counter)+"\n")
    else:
        content.append("There are no scripts defined in this project, so no inheritance statistics can be provided.\n")
    content.append("\n")

    # List script statistics section
    content.append("\n")
    content.append("==== Scripts ====\n")
    if project_scripts_count:
        content.append(f"There are {project_scripts_count} scripts that belong to this project:\n")
        content.append(wiki_list_script_names(project))
    else:
        content.append("There are no scripts defined in this project.\n")
    content.append("\n")


def content(context:AppContext) -> list[str]:
    content:list[str] = []

    # Write the wiki page header.
    content.append("= Projects =\n")
    content.append("This page lists all Papyrus project information for each import.\n")
    content.append("\n\n")

    # Write each project wiki section.
    for identifier in context.papyrus.projects:
        configuration = context.configurations[identifier]
        if not configuration.publish.enable:
            logging.info(f"[{identifier}] has disabled publishing. Skipping wiki index summary for this project.")
            continue

        project:PapyrusProject = context.papyrus.projects[identifier]
        write_section(content, project)
        content.append("\n\n")
    return content


def write(context:AppContext, output_file_path:str) -> None:
    lines:list[str] = content(context)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
