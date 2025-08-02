"""
Generates a MediaWiki page that summarizes information about all Papyrus projects.
"""
import logging
from collections import Counter
from collections.abc import ItemsView
from scribe.app.settings import AppSettings, ProviderProject
from scribe.papyrus.context import PapyrusContext
from scribe.papyrus.project import PapyrusProject
from scribe.wiki.data.article import ArticleType
from scribe.wiki.data.page import Page
from scribe.bots.generator.constants import Wiki
from scribe.bots.generator.scripts_statistics import PapyrusStatistics

class PageIndex:
    """
    Generates a MediaWiki page that summarizes information about all Papyrus projects.
    """

    PAGE_TITLE:str = "Papyrus Projects Index"


    @staticmethod
    def create(file_path:str, settings:AppSettings, papyrus:PapyrusContext) -> 'Page':
        this:Page = Page()
        this.type = ArticleType.Main
        this.file_path = file_path
        this.title = PageIndex.PAGE_TITLE
        this.categories.append(Wiki.CATEGORY_PAPYRUS)

        # Write the wiki page header.
        this.content.append("= Projects =\n")
        this.content.append("This page lists all Papyrus project information for each import.\n")
        this.content.append("\n\n")

        # Write each project wiki section.
        for identifier in papyrus.projects:
            configuration:ProviderProject = settings.configurations[identifier]
            if not configuration.publish.enable:
                logging.info(f"[{identifier}] has disabled publishing. Skipping wiki index summary for this project.")
                continue

            project:PapyrusProject = papyrus.projects[identifier]
            PageIndex.write_section(this, project)
            this.content.append("\n\n")

        return this


    @staticmethod
    def write_section(this:Page, project:PapyrusProject) -> None:
        statistics:PapyrusStatistics = PapyrusStatistics.create(project)

        # Add project summary information
        this.content.append(f"== {project.identifier} ==\n")
        this.content.append(f"* Imports: {statistics.project_imports_count} ({PageIndex.wiki_list_project_imports(project)})\n")
        this.content.append(f"* Scripts: {statistics.project_scripts_count}\n")
        this.content.append("\n")

        # Add script member statistics section
        this.content.append("==== Member Statistics ====\n")
        if statistics.project_scripts_count:
            this.content.append(f"This project overall contains {statistics.script_member_kind_counter.total()} total members spread over {statistics.project_scripts_count} scripts.\n")
            this.content.append(PageIndex.wiki_list_member_kinds(statistics.script_member_kind_counter)+"\n")
        else:
            this.content.append("There are no scripts defined in this project, so no member statistics can be provided.\n")
        this.content.append("\n")

        # Add script inheritance statistics section
        this.content.append("==== Inheritance Statistics ====\n")
        if statistics.project_scripts_count:
            this.content.append(f"The most common extended parent scripts:\n")
            this.content.append(PageIndex.wiki_list_extends_most_common(statistics.script_extends_counter)+"\n")
        else:
            this.content.append("There are no scripts defined in this project, so no inheritance statistics can be provided.\n")
        this.content.append("\n")

        # List script statistics section
        this.content.append("\n")
        this.content.append("==== Scripts ====\n")
        if statistics.project_scripts_count:
            this.content.append(f"There are {statistics.project_scripts_count} scripts that belong to this project:\n")
            this.content.append(PageIndex.wiki_list_script_names(project))
        else:
            this.content.append("There are no scripts defined in this project.\n")
        this.content.append("\n")


    # MediaWiki
    #---------------------------------------------

    @staticmethod
    def wiki_list_project_imports(project:PapyrusProject) -> str:
        return ", ".join(project.imports) if project.imports else "Nothing"


    @staticmethod
    def wiki_list_member_kinds(script_member_kind_counter:Counter[str]) -> str:
        kinds:ItemsView[str, int] = script_member_kind_counter.items()
        if not kinds:
            return "There are no members defined in this project."
        entries:list[str] = []
        for kind, count in kinds:
            entries.append(f"* {kind} was used {count} times.")
        return "\n".join(entries)


    @staticmethod
    def wiki_list_extends_most_common(script_extends_counter:Counter[str]) -> str:
        common_parent_names:list[tuple[str, int]] = script_extends_counter.most_common(3)
        if not common_parent_names:
            return "There are no common scripts in this project."
        entries:list[str] = []
        for script_name, count in common_parent_names:
            entries.append(f"* The {Wiki.link_script_object(script_name)} script was extended {count} times.")
        return "\n".join(entries)


    @staticmethod
    def wiki_list_script_names(project:PapyrusProject) -> str:
        if not project.scripts:
            return "There are no scripts defined in this project."
        entries:list[str] = []
        for script in project.scripts:
            entries.append(f"* {Wiki.link_script_object(str(script.header.name))}")
        return "\n".join(entries)
