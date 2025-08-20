"""
Generates a MediaWiki page that summarizes information about all Papyrus projects.
"""
import logging
from collections import Counter
from collections.abc import ItemsView
from sharp.collections import KeyedCollection
from papyrus.client import PapyrusClient
from papyrus.project import PapyrusProject
from wiki.data.section import SectionLevel
from scribe.publisher.configuration import PublishPapyrus
from scribe.composer.article import Article
from scribe.composer.builder import ArticleBuilder
from scribe.composer.wiki import Wiki
from .scripts_statistics import PapyrusStatistics

class PageIndex:
    """
    Generates a MediaWiki page that summarizes information about all Papyrus projects.
    """

    PAGE_NAME:str = "Script_Information"


    @staticmethod
    def create(wiki:Wiki, jobs:KeyedCollection[str, PublishPapyrus], papyrus:PapyrusClient) -> Article:
        builder:ArticleBuilder = ArticleBuilder(wiki)
        builder.title(PageIndex.PAGE_NAME, Wiki.NAMESPACE_MODDING)
        builder.category(Wiki.CATEGORY_PAPYRUS.name)
        builder.line("This page lists all Papyrus project information for each import.\n")
        builder.line("\n\n")

        # Write each project wiki section.
        for identifier in papyrus.projects:
            job:PublishPapyrus = jobs[identifier]
            if not job.publish.enable:
                logging.info(f"[{identifier}] has disabled publishing. Skipping wiki index summary for this project.")
                continue

            project:PapyrusProject = papyrus.projects[identifier]
            PageIndex.project(builder, project)
            builder.line("\n\n")

        return builder.build()


    @staticmethod
    def project(builder:ArticleBuilder, project:PapyrusProject) -> None:
        # Create statistics for the given project.
        statistics:PapyrusStatistics = PapyrusStatistics.create(project)

        # Add project summary information
        builder.section(project.identifier, SectionLevel.H3)
        builder.line(f"* Imports: {statistics.project_imports_count} ({PageIndex.wiki_list_project_imports(project)})\n")
        builder.line(f"* Scripts: {statistics.project_scripts_count}\n")
        builder.line("\n")

        # Add script member statistics section
        builder.section("Member Statistics", SectionLevel.H4)
        if statistics.project_scripts_count:
            builder.line(f"This project overall contains {statistics.script_member_kind_counter.total()} total members spread over {statistics.project_scripts_count} scripts.\n")
            builder.line(PageIndex.wiki_list_member_kinds(statistics.script_member_kind_counter)+"\n")
        else:
            builder.line("There are no scripts defined in this project, so no member statistics can be provided.\n")
        builder.line("\n")

        # Add script inheritance statistics section
        builder.section("Inheritance Statistics", SectionLevel.H4)
        if statistics.project_scripts_count:
            builder.line(f"The most common extended parent scripts:\n")
            builder.line(PageIndex.wiki_list_extends_most_common(statistics.script_extends_counter)+"\n")
        else:
            builder.line("There are no scripts defined in this project, so no inheritance statistics can be provided.\n")
        builder.line("\n")

        # List script statistics section
        builder.line("\n")
        builder.section("Scripts", SectionLevel.H4)
        if statistics.project_scripts_count:
            builder.line(f"There are {statistics.project_scripts_count} scripts that belong to this project:\n")
            builder.line(PageIndex.wiki_list_script_names(project))
        else:
            builder.line("There are no scripts defined in this project.\n")
        builder.line("\n")


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
