"""
Used to generate wiki page content.
"""
import logging
import os
from sharp.collections import KeyedCollection
from papyrus.client import PapyrusClient
from papyrus.project import PapyrusProject
from papyrus.code import Member, Script
from scribe.app.configuration import AppConfiguration
from scribe.app.context import AppContext
from scribe.composer.article import Article
from scribe.composer.article_text import ArticleText
from scribe.composer.wiki import Wiki
from scribe.generators.pages_index import PageIndex
from scribe.generators.pages_member import PageMember
from scribe.generators.pages_script import PageScript
from scribe.publisher.configuration import PublishPapyrus
from scribe.publisher.publishing import Sort
from scribe.services.composer import ComposerService
from scribe.services.papyrus import PapyrusService
from scribe.services.publisher import PublisherService

class GeneratorService:
    """
    The service responsible for generating wiki pages from Papyrus projects.
    """

    NAME:str = "Generator"
    """The name of this service."""

    DIV_WIDTH:int = 50
    """The width of divider lines in the log output."""

    PAGE_SCRIPT_INDEX_FILE_NAME:str = "Script_Information.wiki"
    """The file name of the wiki page that summarizes all scripts in a Papyrus project."""


    @staticmethod
    def start(app:AppContext) -> bool:
        logging.info(f"{GeneratorService.NAME} - Starting")

        try:
            publisher:PublisherService = PublisherService.create(app.configuration)
        except Exception as exception:
            logging.error(f"Aborting program. Failed to start publisher service. {exception}")
            return False

        try:
            papyrus:PapyrusService = PapyrusService.create(publisher)
        except Exception as exception:
            logging.error(f"Aborting program. Failed to start Papyrus service. {exception}")
            return False

        try:
            composer:ComposerService = ComposerService.create(app.configuration)
        except Exception as exception:
            logging.error(f"Aborting program. Failed to start composer service. {exception}")
            return False

        GeneratorService.wiki_start(app.configuration, publisher, papyrus, composer)
        composer.save()
        return True


    # Wiki
    #---------------------------------------------

    @staticmethod
    def wiki_start(configuration:AppConfiguration, publisher:PublisherService, papyrus:PapyrusService, composer:ComposerService) -> None:
        """
        Start the wiki generation process.
        """
        jobs:KeyedCollection[str, PublishPapyrus] = publisher.get_papyrus()

        # Generate the wiki index summary page.
        index_page:Article = Generate_Wiki.wiki_page_create_index(composer.wiki, configuration, papyrus.client, jobs)
        composer.wiki.articles.add(index_page)

        # Generate wiki pages for each project.
        logging.info("Wiki Generation ".center(GeneratorService.DIV_WIDTH, "-"))
        logging.info(f"Writing wiki pages for {len(jobs)} configurations.")
        for job in jobs.values():
            if not GeneratorService.wiki_projects(composer, papyrus, job):
                logging.error(f"[{job.identifier}] Failed to generate one or more wiki pages.")


    @staticmethod
    def wiki_projects(composer:ComposerService, papyrus:PapyrusService, job:PublishPapyrus) -> bool:

        # TODO: Ensure invalid jobs with not enough info dont get this far, like the `Game` key.
        # Exception has occurred: KeyError
        # 'Game'
        project:PapyrusProject|None = papyrus.client.projects.get(job.identifier)
        if not project:
            logging.warning(f"[{job.identifier}] Skipping this job. No matching Papyrus project was found in the Papyrus context.")
            return False

        # Skip any disabled projects.
        if not job.publish.enable:
            logging.info(f"[{project.identifier}] has disabled publishing. Skipping wiki page generation.")
            return True # Not an error, successfully did nothing.

        # Skip any projects without a publish sorting option.
        if not job.publish.sort:
            logging.warning(f"[{project.identifier}] Skipping this Papyrus project. The project publish sorting property cannot be a None value.")
            return False

        # Validate provided project configuration.
        if not project.root or not job.publish.output:
            logging.warning(f"[{project.identifier}] Skipping this Papyrus project. The path values were not set in the project options.")
            return False

        # Ensure the project input directory exist, else skip.
        if not os.path.exists(project.root):
            logging.warning(f"[{project.identifier}] Skipping this Papyrus project. The project `root` directory does not exist: '{project.root}'")
            return False

        # Wiki: Generate wiki pages for each project script.
        for script in project.scripts:
            script_file_name:str = script.header.name.file_name()
            script_file_path:str = script.header.name.file_path()
            script_file_path_full:str = os.path.join(project.root, f"{script_file_path}.psc")

            # Get the output file path based on the project sorting option.
            output_file_path:str = ""
            if job.publish.sort == Sort.DEFAULT:
                output_file_path = os.path.join(job.publish.output, f"{script_file_path}.wiki")
            elif job.publish.sort == Sort.FLAT:
                output_file_path = os.path.join(job.publish.output, f"{str(script.header.name).replace(":", "-")}.wiki")
            elif job.publish.sort == Sort.TREE:
                output_file_path = os.path.join(job.publish.output, script_file_path+".psc", f"{script_file_name}.wiki")
            else:
                logging.warning(f"[{project.identifier}][{script_file_path}] Skipping this script. The project sorting property could not be determined.")
                continue

            # Create the project output directory.
            output_file_directory:str = os.path.dirname(output_file_path)
            if not os.path.exists(output_file_directory):
                os.makedirs(output_file_directory)
                logging.debug(f"[{project.identifier}][{script_file_path}] Created the output directory: {output_file_directory}")

            # Write a wiki page for this script object.
            if job.publish.enable_objects:
                script_page:Article = Generate_Wiki.wiki_page_create_script(composer.wiki, output_file_path, papyrus.client, project, script)
                composer.wiki.articles.add(script_page)
                logging.debug(f"[{project.identifier}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

            # Write a wiki page for this script member.
            if job.publish.enable_members:
                for key in script.members:
                    member:Member = script.members[key]
                    member_file_name:str = f"{script_file_name}-{member.name}.wiki"
                    member_file_path:str = os.path.join(os.path.dirname(output_file_path), member_file_name)
                    script_member_page:Article = Generate_Wiki.wiki_page_create_script_member(composer.wiki, member_file_path, project, script, member)
                    composer.wiki.articles.add(script_member_page)
                    logging.debug(f"[{project.identifier}]<{script_file_path}>::{member.name} -> {member_file_path}")

        return True



# Temporary Organization (Developer)
#---------------------------------------------

class Generate_Wiki:

    @staticmethod
    def wiki_page_create_index(wiki:Wiki, configuration:AppConfiguration, papyrus:PapyrusClient, jobs:KeyedCollection[str, PublishPapyrus]) -> Article:
        if not configuration.export_directory:
            raise ValueError("The export directory for wiki pages is not set in the application configuration.")

        page:Article = PageIndex.create(wiki, jobs, papyrus)
        page_file_path:str = os.path.join(configuration.export_directory, GeneratorService.PAGE_SCRIPT_INDEX_FILE_NAME)
        try:
            ArticleText.compose_save(page, page_file_path)
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def wiki_page_create_script(wiki:Wiki, file_path:str, papyrus:PapyrusClient, project:PapyrusProject, script:Script) -> Article:
        page:Article = PageScript.create(wiki, papyrus, project, script)
        try:
            ArticleText.compose_save(page, file_path)
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def wiki_page_create_script_member(wiki:Wiki, file_path:str, project:PapyrusProject, script:Script, member:Member) -> Article:
        page:Article = PageMember.create(wiki, file_path, project, script, member)
        try:
            ArticleText.compose_save(page, file_path)
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page
