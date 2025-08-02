"""
Used to upload wiki pages to a remote site.
"""
from http import HTTPStatus
import logging
import os
from scribe.app.context import AppContext
from scribe.wiki.data.page import Page
from scribe.wiki.web.client import WebClient
from scribe.wiki.web.credentials import Credential, create_credentials
from scribe.wiki.web.site import Site, create_site
from scribe.wiki.web.api.edit import EditResponse
from scribe.wiki.web.api.login import LoginResponse
from scribe.wiki.web.api.status import EditResult, LoginStatus
from scribe.bots.generator.context import GeneratorContext

class UploadService:
    """
    The service responsible for uploading wiki pages to a remote site.
    """

    BOT_EDIT_SUMMARY:str = "This edit was made by Scribe Bot using the wiki API."


    @staticmethod
    def start(app:AppContext) -> None:
        if not app.wiki.articles:
            logging.error("No wiki pages to upload.")
            return

        if not app.settings.environment:
            logging.error("No environment specified.")
            return

        if not app.settings.upload_configuration_file:
            logging.error("No upload configuration specified.")
            return

        # Load wiki context from file
        wiki_file_path:str = os.path.join(app.settings.export_directory, GeneratorContext.FILENAME)
        try:
            app.wiki = GeneratorContext.load(wiki_file_path)
            logging.info(f"Loaded {len(app.wiki.articles)} pages from wiki.")
        except FileNotFoundError as fileNotFoundError:
            logging.error(f"Wiki file not found: '{fileNotFoundError}'")
            return


        # Create site and client
        site:Site = create_site(app.settings.upload_configuration_file, app.settings.environment)
        credential:Credential = create_credentials()
        client:WebClient = WebClient(site)

        # Login to the site
        try:
            login:LoginResponse = client.login(credential.username, credential.password)
        except Exception as exception:
            logging.error(f"Login failed with exception: {exception}")
            return

        if login.status_code != HTTPStatus.OK:
            logging.error(f"HTTP request failed: '{login.status_code}'")
            return
        elif login.status != LoginStatus.PASS:
            logging.error(f"Login failed: '{login.status}'")
            return
        else:
            logging.info(f"Login successfull for '{credential.username}' user.")

        # Upload each page
        for article in app.wiki.articles:
            if isinstance(article, Page):
                UploadService.edit_page(client, article, UploadService.BOT_EDIT_SUMMARY)
            else:
                logging.warning(f"Skipping upload for non-page article: '{article.title}'")


    @staticmethod
    def edit(client:WebClient, title:str, text:str, summary:str) -> None:
        edit:EditResponse = client.edit(title, text, summary)
        if not edit:
            logging.error("The 'edit' response was None.")
            return
        elif edit.status_code != HTTPStatus.OK:
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
    def edit_page(client:WebClient, page:Page, summary:str) -> None:
        UploadService.edit(client, page.title, str(page.content), summary)
