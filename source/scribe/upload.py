"""
Used to upload wiki pages to a remote site.
"""
import logging
import os
from typing import override
from http import HTTPStatus
from sharp.objects import Dump
from wiki.web.client import WebClient
from wiki.web.credentials import Credential
from wiki.web.site import Site
from wiki.web.api.edit import EditResponse
from wiki.web.api.login import LoginResponse
from wiki.web.api.types import EditResult, LoginStatus
from scribe.app.context import AppContext
from scribe.publisher.article import Article
from scribe.publisher.wiki import Wiki
from scribe.publisher.wiki_json import WikiJson

class UploadService:
    """
    This service is responsible for uploading wiki pages to a remote site.
    """

    NAME:str = "Uploader"
    """The name of this service."""

    BOT_EDIT_SUMMARY:str = "This edit was made by Scribe Bot using the wiki API."
    """The bot edit summary used for uploads."""

    USE_DRY_RUN:bool = False
    """ When True, the upload will not actually be performed."""


    def __init__(self) -> None:
        super().__init__()


    @override
    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def start(app:AppContext) -> bool:
        if not app.configuration.export_directory:
            logging.error("No export directory specified.")
            return False

        if not app.configuration.uploader_environment:
            logging.error("No environment specified.")
            return False

        if not app.configuration.uploader_file_path:
            logging.error("No upload configuration specified.")
            return False

        this:UploadService = UploadService()
        logging.info(f"{UploadService.NAME} - Starting")
        logging.debug(str(this))

        # Load wiki context from file
        wiki:Wiki = Wiki.create()
        wiki_file_path:str = os.path.join(app.configuration.export_directory, WikiJson.JSON_FILENAME)
        try:
            wiki = WikiJson.load(wiki, wiki_file_path)
            logging.info(f"Loaded {len(wiki.articles)} pages from wiki.")

        except FileNotFoundError as fileNotFoundError:
            logging.error(f"Wiki file not found: '{fileNotFoundError}'")
            return False

        if not wiki.articles:
            logging.error("No wiki articles to upload.")
            return False

        # Create site and client
        site:Site = Site.create(app.configuration.uploader_file_path, app.configuration.uploader_environment)
        credential:Credential = Credential.create()
        client:WebClient = WebClient(site)

        # Login to the site
        try:
            login:LoginResponse = client.login(credential.username, credential.password)
        except Exception as exception:
            logging.error(f"Login failed with exception: {exception}")
            return False

        if login.status_code != HTTPStatus.OK:
            logging.error(f"HTTP request failed: '{login.status_code}'")
            return False
        elif login.status != LoginStatus.PASS:
            logging.error(f"Login failed: '{login.status}'")
            return False
        else:
            logging.info(f"Login successfull for '{credential.username}' user.")

        if UploadService.USE_DRY_RUN:
            logging.info("Dry run mode enabled. No edits will be made.")
            return False

        # Upload each page
        for article in wiki.articles.values():
            UploadService.edit_article(client, article, UploadService.BOT_EDIT_SUMMARY)

        return True


    @staticmethod
    def edit(client:WebClient, title:str, text:str, summary:str) -> None:
        edit:EditResponse = client.edit(title, text, summary)
        if edit.status_code != HTTPStatus.OK:
            logging.error(f"The 'edit' http request failed with status code: {edit.status_code}")
            return
        elif edit.result != EditResult.SUCCESS:
            logging.error(f"The 'edit' result failed: {edit.result}")
            return

        if edit.revision:
            logging.info(f"The 'edit' result for revision {edit.revision} was successful: {edit.response.content}")
        else:
            logging.warning(f"The 'edit' resulted in no changes: {edit.response.content}")


    @staticmethod
    def edit_article(client:WebClient, article:Article, summary:str) -> None:
        composed:list[str] = article.compose()
        content:str = "".join(composed)
        UploadService.edit(client, article.title.value, content, summary)
