"""
Used to upload wiki pages to a remote site.
"""
import logging
import os
from typing import Any, override
from http import HTTPStatus
from scribe.app.context import AppContext
from scribe.shared.objects import Dump
from scribe.wiki.data.article import Article
from scribe.wiki.data.client import ArticleClient
from scribe.wiki.web.client import WebClient
from scribe.wiki.web.credentials import Credential, create_credentials
from scribe.wiki.web.site import Site, create_site
from scribe.wiki.web.api.edit import EditResponse
from scribe.wiki.web.api.login import LoginResponse
from scribe.wiki.web.api.types import EditResult, LoginStatus

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
        self.wiki:ArticleClient = ArticleClient()


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
        wiki_file_path:str = os.path.join(app.configuration.export_directory, ArticleClient.JSON_FILENAME)
        try:
            this.wiki = ArticleClient.load(wiki_file_path)
            logging.info(f"Loaded {len(this.wiki.articles)} pages from wiki.")

        except FileNotFoundError as fileNotFoundError:
            logging.error(f"Wiki file not found: '{fileNotFoundError}'")
            return False

        if not this.wiki.articles:
            logging.error("No wiki articles to upload.")
            return False

        # Create site and client
        site:Site = create_site(app.configuration.uploader_file_path, app.configuration.uploader_environment)
        credential:Credential = create_credentials()
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
        for article in this.wiki.articles.values():
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
        UploadService.edit(client, article.title, content, summary)


    # Serialization
    #---------------------------------------------

    def data_encode(self) -> dict[str, Any]:
        """The data encoder for this class."""
        data:dict[str, Any] = {
            "wiki": self.wiki.data_encode()
        }
        return data


    @staticmethod
    def data_decode(data:dict[str, Any]) -> 'UploadService':
        """The data decoder for this class."""
        this:UploadService = UploadService()
        wiki_articles_data:dict[str, Any] = data.get("wiki", {})
        this.wiki = ArticleClient.data_decode(wiki_articles_data)
        return this
