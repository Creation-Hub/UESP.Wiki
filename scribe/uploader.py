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

class UploadService:
    """
    The service responsible for uploading wiki pages to a remote site.
    """

    # Service
    #---------------------------------------------

    @staticmethod
    def start(app:AppContext) -> None:
        if not app.settings.environment:
            logging.error("No environment specified.")
            return

        if not app.arguments.upload_configuration_file:
            logging.error("No upload configuration specified.")
            return

        site:Site = create_site(app.arguments.upload_configuration_file, app.settings.environment)
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
            logging.info(f"Login successfull for '{credential.username}'.")


        # Begin making page edits

        client.edit("User:Scrivener07", "My name is Scrivener and I have been modding since TES4 Oblivion.", "This is a test edit made by Scrivener07's bot." )

        edit:EditResponse = client.edit("User:Scrivener07/Bot", "This is a test edit made by Scrivener07's bot.", "This is a test edit that uses the API." )
        if edit.status_code == HTTPStatus.OK:
            logging.info("Edit request was successful.")
        else:
            logging.error(f"Edit request failed with status code: {edit.status_code}")
            return

        if edit.result == EditResult.SUCCESS:
            logging.info("Edit was successful.")
        else:
            logging.error(f"Edit failed with result: {edit.result}")
            return

        if edit.revision:
            logging.info(f"Edit successful! New revision ID: {edit.revision}")
        else:
            logging.warning(f"No new revision ID returned: {edit.response.content}")
