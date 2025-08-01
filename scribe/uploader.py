"""
Used to upload wiki pages to a remote site.
"""
from http import HTTPStatus
import logging
from scribe.app.context import AppContext
from scribe.web.client import Client
from scribe.web.credentials import Credential, create_credentials
from scribe.web.site import Site, create_site
from scribe.web.api.edit import EditResponse
from scribe.web.api.login import LoginResponse
from scribe.web.api.status import EditResult, LoginStatus
from scribe.wiki.page import Page

class UploadService:
    """
    The service responsible for uploading wiki pages to a remote site.
    """

    BOT_EDIT_SUMMARY:str = "This edit was made by Scribe Bot using the wiki API."


    @staticmethod
    def start(app:AppContext) -> None:
        if not app.settings.environment:
            logging.error("No environment specified.")
            return

        if not app.settings.upload_configuration_file:
            logging.error("No upload configuration specified.")
            return

        site:Site = create_site(app.settings.upload_configuration_file, app.settings.environment)
        credential:Credential = create_credentials()
        client:Client = Client(site)

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

        user_page:Page = Page()
        user_page.file_path = "User-Scrivener07.wiki"
        user_page.title = "User:Scrivener07"
        user_page.content = ["My name is Scrivener and I have been modding since TES4 Oblivion."]
        app.wiki.pages.append(user_page)

        bot_page:Page = Page()
        bot_page.file_path = "User-Scrivener07-Bot.wiki"
        bot_page.title = "User:Scrivener07/Bot"
        bot_page.content = ["This is the Scribe Bot wiki page."]
        app.wiki.pages.append(bot_page)

        if not app.wiki.pages:
            logging.error("No wiki pages to upload.")
            return

        for page in app.wiki.pages:
            UploadService.edit_page(client, page, UploadService.BOT_EDIT_SUMMARY)


    @staticmethod
    def edit(client:Client, title:str, text:str, summary:str) -> None:
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
    def edit_page(client:Client, page:Page, summary:str) -> None:
        UploadService.edit(client, page.title, str(page.content), summary)
