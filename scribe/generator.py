"""
Used to generate wiki page content.
"""
import json
import os
import logging
from typing import Any
from scribe.app.configuration import AppConfiguration
from scribe.app.context import AppContext
from scribe.app.settings import AppSettings
from scribe.shared.objects import Dump
from scribe.papyrus.client import PapyrusClient
from scribe.papyrus.project import PapyrusProject
from scribe.papyrus.code import Member, Script
from scribe.wiki.data.article import ArticleType
from scribe.wiki.data.article_text import ArticleText
from scribe.wiki.data.client import DataClient
from scribe.wiki.data.page import Page
from scribe.wiki.data.template import Template
from scribe.bots.publishing import Sort
from scribe.bots.provider import Provider, ProviderProject
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


    def __init__(self) -> None:
        self.papyrus:PapyrusClient = PapyrusClient()
        """The Papyrus client used to load and manage Papyrus projects."""

        self.wiki:DataClient = DataClient()
        """The wiki client used to manage wiki pages."""

        self.providers:dict[str, Provider] = {}
        """The providers loaded from the settings file."""

        self.configurations:dict[str, ProviderProject] = {}
        """The app configurations loaded from the settings file."""


    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def start(app:AppContext) -> bool:
        this:GenerateService = GenerateService()
        logging.info(f"{GenerateService.NAME} - Starting service {str(this)}")

        if not app.configuration:
            logging.error(f"Aborting program. No application configuration found.")
            return False

        if not app.settings:
            logging.error(f"Aborting program. No application settings found.")
            return False

        # Start the Papyrus context.
        if not GenerateService.papyrus_start(app.configuration, this.papyrus, this.configurations):
            logging.error(f"Aborting program. Failed start Papyrus.")
            return False

        # Start the wiki context.
        if not GenerateService.wiki_start(app.configuration, this.wiki, this.papyrus, this.configurations):
            logging.error(f"Aborting program. Failed to generate wiki pages.")
            return False

        return True


    # JSON
    #---------------------------------------------

    @staticmethod
    def json_load(file_path:str) -> 'GenerateService':
        """
        Reads the given application settings file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")
        with open(file_path, encoding="utf-8") as file:
            data:dict[str, Any] = json.load(file)
        return GenerateService.json_decode(data)


    @staticmethod
    def json_decode(data:dict[str, Any]) -> 'GenerateService':
        this:GenerateService = GenerateService()
        this.configurations = GenerateService.json_decode_providers(data)
        return this


    # TODO: WIP
    @staticmethod
    def json_decode_providers(data:dict[str, Any]) -> dict[str, ProviderProject]:
        providers:dict[str, Provider] = {}
        configurations:dict[str, ProviderProject] = {}

        # Read the provider configurations.
        data_providers:list[Any] = data.get("providers", [])
        for data_provider in data_providers:
            data_provider:dict[str, Any] = data_provider
            provider:Provider = Provider.json_decode(data_provider)
            providers[provider.identifier] = provider

            # Read the configuration for projects.
            data_projects:list[Any] = data_provider.get("projects", [])
            for data_project in data_projects:
                data_project:dict[str, Any] = data_project
                configuration:ProviderProject = ProviderProject.json_decode(data_project)
                configurations[configuration.identifier] = configuration

        return configurations


    # Papyrus
    #---------------------------------------------

    @staticmethod
    def papyrus_start(app_configuration:AppConfiguration, papyrus:PapyrusClient, configurations:dict[str, ProviderProject]) -> bool:
        """
        Start the Papyrus context and load all projects.
        """
        # Load each configuration.
        logging.info(" Configurations ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Found {len(configurations)} configurations.")
        for key in configurations:
            providerProject:ProviderProject = configurations[key]

            # Ensure the project root directory exists, else skip.
            if not providerProject.root:
                logging.warning(f"[{providerProject.identifier}] Skipping this project. The path values were not set in the project options.")
                continue
            elif not os.path.exists(providerProject.root):
                logging.warning(f"[{providerProject.identifier}] Skipping this project. The project `root` directory does not exist: '{providerProject.root}'")
                continue

            # Create a Papyrus project for this configuration.
            project:PapyrusProject = PapyrusProject()
            project.identifier = providerProject.identifier
            project.imports = providerProject.imports
            project.root = providerProject.root

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
    def wiki_start(app_configuration:AppConfiguration, wiki:DataClient, papyrus:PapyrusClient, configurations:dict[str, ProviderProject]) -> bool:
        """
        Start the wiki generation process.
        """
        user_page:Page = Page() # This is for debug purposes.
        user_page.type = ArticleType.User
        user_page.title = "User:Scrivener07"
        user_page.content = ["My name is Scrivener and I have been modding since TES4 Oblivion."]
        user_page.categories = []
        wiki.add(user_page)

        bot_page:Page = Page() # This is for debug purposes.
        bot_page.type = ArticleType.User
        bot_page.title = "User:Scrivener07/Bot"
        bot_page.content = ["This is the Scribe Bot wiki page."]
        user_page.categories = []
        wiki.add(bot_page)


        # Generate the wiki index summary page.
        index_page:Page = GenerateWiki.wiki_page_create_index(configurations, app_configuration, papyrus)
        wiki.add(index_page)

        # Generate wiki pages for each project.
        logging.info("Wiki Generation ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Writing wiki pages for {len(configurations)} configurations.")
        for key in configurations:
            configuration:ProviderProject = configurations[key]
            if not GenerateService.wiki_projects(wiki, papyrus, configuration):
                logging.error(f"[{configuration.identifier}] Failed to generate one or more wiki pages.")


        if not app_configuration.export_directory:
            raise ValueError("The export directory for wiki pages is not set in the application configuration.")

        # Save the wiki file
        wiki_file_path:str = os.path.join(app_configuration.export_directory, AppSettings.WIKI_JSON_FILENAME)
        wiki.save(wiki_file_path)
        logging.info(f"Saved wiki: '{wiki_file_path}'")
        return True


    @staticmethod
    def wiki_projects(wiki:DataClient, papyrus:PapyrusClient, configuration:ProviderProject) -> bool:
        project:PapyrusProject = papyrus.projects[configuration.identifier]

        # Skip any disabled projects.
        if not configuration.publish.enable:
            logging.info(f"[{project.identifier}] has disabled publishing. Skipping wiki page generation.")
            return True # Not an error, successfully did nothing.

        # Skip any projects without a publish sorting option.
        if not configuration.publish.sort:
            logging.warning(f"[{project.identifier}] Skipping this project. The project publish sorting property cannot be a None value.")
            return False

        # Validate provided project configuration.
        if not project.root or not configuration.publish.output:
            logging.warning(f"[{project.identifier}] Skipping this project. The path values were not set in the project options.")
            return False

        # Ensure the project input directory exist, else skip.
        if not os.path.exists(project.root):
            logging.warning(f"[{project.identifier}] Skipping this project. The project `root` directory does not exist: '{project.root}'")
            return False

        # Wiki: Generate wiki pages for each project script.
        for script in project.scripts:
            script_file_name:str = script.header.name.file_name()
            script_file_path:str = script.header.name.file_path()
            script_file_path_full:str = os.path.join(project.root, f"{script_file_path}.psc")

            # Get the output file path based on the project sorting option.
            output_file_path:str = ""
            if configuration.publish.sort == Sort.DEFAULT:
                output_file_path = os.path.join(configuration.publish.output, f"{script_file_path}.wiki")
            elif configuration.publish.sort == Sort.FLAT:
                output_file_path = os.path.join(configuration.publish.output, f"{str(script.header.name).replace(":", "-")}.wiki")
            elif configuration.publish.sort == Sort.TREE:
                output_file_path = os.path.join(configuration.publish.output, script_file_path+".psc", f"{script_file_name}.wiki")
            else:
                logging.warning(f"[{project.identifier}][{script_file_path}] Skipping this script. The project sorting property could not be determined.")
                continue

            # Create the project output directory.
            output_file_directory:str = os.path.dirname(output_file_path)
            if not os.path.exists(output_file_directory):
                os.makedirs(output_file_directory)
                logging.debug(f"[{project.identifier}][{script_file_path}] Created the output directory: {output_file_directory}")

            # Write a wiki page for this script object.
            if configuration.publish.enable_objects:
                script_page:Page = GenerateWiki.wiki_page_create_script(output_file_path, papyrus, project, script)
                wiki.add(script_page)
                logging.debug(f"[{project.identifier}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

            # Write a wiki page for this script member.
            if configuration.publish.enable_members:
                for key in script.members:
                    member:Member = script.members[key]
                    member_file_name:str = f"{script_file_name}-{member.name}.wiki"
                    member_file_path:str = os.path.join(os.path.dirname(output_file_path), member_file_name)
                    script_member_page:Page = GenerateWiki.wiki_page_create_script_member(member_file_path, project, script, member)
                    wiki.add(script_member_page)
                    logging.debug(f"[{project.identifier}]<{script_file_path}>::{member.name} -> {member_file_path}")

        return True



class GenerateWiki:

    # Wiki: Page
    #---------------------------------------------

    @staticmethod
    def wiki_page_create_index(configurations:dict[str, ProviderProject], app_configuration:AppConfiguration, papyrus:PapyrusClient) -> Page:
        if not app_configuration.export_directory:
            raise ValueError("The export directory for wiki pages is not set in the application configuration.")

        page:Page = PageIndex.create(configurations, papyrus)
        page_file_path:str = os.path.join(app_configuration.export_directory, GenerateService.PAGE_SCRIPT_INDEX_FILE_NAME)
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


    # Wiki: Template
    #---------------------------------------------

    @staticmethod
    def wiki_template_script_object_summary(papyrus:PapyrusClient, project:PapyrusProject, script:Script, game_version:str) -> Template:
        raise NotImplementedError("The `wiki_template_script_object_summary` method is not implemented yet.")
        template:Template = Template()
        template.file_path = "file_path"
        template.title = "Script_Object_Summary"
        template.content = []
        template.categories = [Wiki.CATEGORY_TEMPLATES_INFOBOX]

        content:str = Script_Object_Summary.template(papyrus, project, script, game_version)
        template.content.append(content)

        return template
