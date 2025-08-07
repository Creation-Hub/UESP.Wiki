"""
Used to generate wiki page content.
"""
import json
import os
import logging
from typing import Any, override
from scribe.app.configuration import AppConfiguration
from scribe.app.context import AppContext
from scribe.shared.objects import Dump
from scribe.papyrus.client import PapyrusClient
from scribe.papyrus.project import PapyrusProject
from scribe.papyrus.code import Member, Script
from scribe.wiki.data.article import Namespace, Page, Template
from scribe.wiki.data.article_text import ArticleText
from scribe.wiki.data.client import DataClient
from scribe.bots.common import WikiCommon
from scribe.bots.publishing import Sort
from scribe.bots.jobs import JobProvider, Job
from scribe.bots.generator.wiki import Wiki
from scribe.bots.generator.pages_index import PageIndex
from scribe.bots.generator.pages_member import PageMember
from scribe.bots.generator.pages_script import PageScript
from scribe.bots.generator.templates import Script_Object_Summary

class GenerateService:
    """
    The service responsible for generating wiki pages from Papyrus projects.
    """

    NAME:str = "Generator"
    """The name of this service."""

    DIV_WIDTH:int = 50
    """The width of divider lines in the log output."""

    PAGE_SCRIPT_INDEX_FILE_NAME:str = "Script_Information.wiki"
    """The file name of the wiki page that summarizes all scripts in a Papyrus project."""

    JSON_ENCODING:str = "utf-8"


    def __init__(self) -> None:
        super().__init__()

        self.papyrus:PapyrusClient = PapyrusClient()
        """The Papyrus client used to load and manage Papyrus projects."""

        self.wiki:DataClient = DataClient()
        """The wiki client used to manage wiki pages."""

        self.providers:dict[str, JobProvider] = {}
        """The job providers loaded from the settings file."""

        self.jobs:dict[str, Job] = {}
        """All the jobs from all providers consolidated into a single dictionary."""


    @override
    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def start(app:AppContext) -> bool:
        if not app.configuration.generator_file_path:
            logging.error(f"Aborting program. No generator settings file found in the application configuration.")
            return False

        this:GenerateService = Generate_JSON.json_load(app.configuration.generator_file_path)

        # Populate all jobs from all providers.
        for provider in this.providers.values():
            if not provider.jobs: continue
            for key, job in provider.jobs.items():
                this.jobs[key] = job

        logging.info(f"{GenerateService.NAME} - Starting")
        logging.debug(str(this))

        # Start the Papyrus context.
        if not GenerateService.papyrus_start(this.papyrus, this.jobs):
            logging.error(f"Aborting program. Failed to start Papyrus.")
            return False

        # Start the wiki context.
        if not GenerateService.wiki_start(app.configuration, this.wiki, this.papyrus, this.jobs):
            logging.error(f"Aborting program. Failed to generate wiki pages.")
            return False

        return True


    # Papyrus
    #---------------------------------------------

    @staticmethod
    def papyrus_start(papyrus:PapyrusClient, jobs:dict[str, Job]) -> bool:
        """
        Start the Papyrus context and load all projects.
        """
        # Load each configuration.
        logging.info(" Configurations ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Found {len(jobs)} configurations.")
        for job in jobs.values():
            # Ensure the job root directory exists, else skip.
            if not job.root:
                logging.warning(f"[{job.identifier}] Skipping this job. The path values were not set in the job options.")
                continue
            elif not os.path.exists(job.root):
                logging.warning(f"[{job.identifier}] Skipping this job. The job `root` directory does not exist: '{job.root}'")
                continue

            # Create a Papyrus project for this configuration.
            project:PapyrusProject = PapyrusProject()
            project.identifier = job.identifier
            project.imports = job.imports
            project.root = job.root

            # Add project to the Papyrus context.
            papyrus.add(project)
            logging.info(f"[{project.identifier}] Loaded project from configuration.")

        # Ensure that projects exist by loading each.
        logging.info(" Papyrus ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Loading {len(papyrus.projects)} projects.")
        if not papyrus.load():
            logging.error(f"Failed to load one or more Papyrus projects.")
            return False
        else:
            return True


    # Wiki
    #---------------------------------------------

    @staticmethod
    def wiki_start(configuration:AppConfiguration, wiki:DataClient, papyrus:PapyrusClient, jobs:dict[str, Job]) -> bool:
        """
        Start the wiki generation process.
        """
        user_page:Page = Page() # This is for debug purposes.
        user_page.namespace = Namespace.User
        user_page.name = "Scrivener07"
        user_page.content = ["My name is Scrivener and I have been modding since TES4 Oblivion."]
        user_page.categories = []
        wiki.add_article(user_page)

        bot_page:Page = Page() # This is for debug purposes.
        bot_page.namespace = Namespace.User
        bot_page.name = "Scrivener07/Bot"
        bot_page.content = ["This is the Scribe Bot wiki page."]
        user_page.categories = []
        wiki.add_article(bot_page)

        # Generate the wiki index summary page.
        index_page:Page = Generate_Wiki.wiki_page_create_index(configuration, papyrus, jobs)
        wiki.add_article(index_page)

        # Generate wiki pages for each project.
        logging.info("Wiki Generation ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Writing wiki pages for {len(jobs)} configurations.")
        for job in jobs.values():
            if not GenerateService.wiki_projects(wiki, papyrus, job):
                logging.error(f"[{job.identifier}] Failed to generate one or more wiki pages.")

        # Save the wiki file
        if not configuration.export_directory:
            raise ValueError("The export directory for wiki pages is not set in the application configuration.")

        wiki_file_path:str = os.path.join(configuration.export_directory, WikiCommon.WIKI_JSON_FILENAME)
        wiki.save(wiki_file_path)
        logging.info(f"Saved wiki: '{wiki_file_path}'")
        return True


    @staticmethod
    def wiki_projects(wiki:DataClient, papyrus:PapyrusClient, job:Job) -> bool:

        # TODO: Ensure invalid jobs with not enough info dont get this far, like the `Game` key.
        # Exception has occurred: KeyError
        # 'Game'
        project:PapyrusProject|None = papyrus.projects.get(job.identifier)
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
                script_page:Page = Generate_Wiki.wiki_page_create_script(output_file_path, papyrus, project, script)
                wiki.add_article(script_page)
                logging.debug(f"[{project.identifier}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

            # Write a wiki page for this script member.
            if job.publish.enable_members:
                for key in script.members:
                    member:Member = script.members[key]
                    member_file_name:str = f"{script_file_name}-{member.name}.wiki"
                    member_file_path:str = os.path.join(os.path.dirname(output_file_path), member_file_name)
                    script_member_page:Page = Generate_Wiki.wiki_page_create_script_member(member_file_path, project, script, member)
                    wiki.add_article(script_member_page)
                    logging.debug(f"[{project.identifier}]<{script_file_path}>::{member.name} -> {member_file_path}")

        return True


# Temporary Organization (Developer)
#---------------------------------------------

class Generate_JSON:

    @staticmethod
    def json_load(file_path:str) -> GenerateService:
        """
        Reads the given application settings file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")
        with open(file_path, encoding=GenerateService.JSON_ENCODING) as file:
            data:dict[str, Any] = json.load(file)
        return Generate_JSON.json_decode(data)


    @staticmethod
    def json_decode(data:dict[str, Any]) -> GenerateService:
        this:GenerateService = GenerateService()
        this.providers = Generate_JSON.json_decode_providers(data)
        return this


    @staticmethod
    def json_decode_providers(data:dict[str, Any]) -> dict[str, JobProvider]:
        providers:dict[str, JobProvider] = {}
        data_providers:list[Any] = data.get("providers", [])
        for data_provider in data_providers:
            data_provider:dict[str, Any] = data_provider
            provider:JobProvider = JobProvider.json_decode(data_provider)
            providers[provider.identifier] = provider
        return providers


class Generate_Wiki:

    @staticmethod
    def wiki_page_create_index(configuration:AppConfiguration, papyrus:PapyrusClient, projects:dict[str, Job]) -> Page:
        if not configuration.export_directory:
            raise ValueError("The export directory for wiki pages is not set in the application configuration.")

        page:Page = PageIndex.create(projects, papyrus)
        page_file_path:str = os.path.join(configuration.export_directory, GenerateService.PAGE_SCRIPT_INDEX_FILE_NAME)
        try:
            ArticleText.compose_save(page, page_file_path)
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def wiki_page_create_script(file_path:str, papyrus:PapyrusClient, project:PapyrusProject, script:Script) -> Page:
        page:Page = PageScript.create(file_path, papyrus, project, script)
        try:
            ArticleText.compose_save(page, file_path)
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def wiki_page_create_script_member(file_path:str, project:PapyrusProject, script:Script, member:Member) -> Page:
        page:Page = PageMember.create(file_path, project, script, member)
        try:
            ArticleText.compose_save(page, file_path)
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def _wiki_template_script_object_summary(papyrus:PapyrusClient, project:PapyrusProject, script:Script, game_version:str) -> Template:
        template:Template = Template()
        template.name = "Script_Object_Summary"
        template.content = []
        template.categories = [Wiki.CATEGORY_TEMPLATES_INFOBOX]

        content:str = Script_Object_Summary.template(papyrus, project, script, game_version)
        template.content.append(content)

        raise NotImplementedError("The `wiki_template_script_object_summary` method is not implemented yet.")
        # return template
