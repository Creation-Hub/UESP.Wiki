from http import HTTPStatus
import os
from uesp.web.clients.client import Client
from uesp.web.clients.credentials import Credential, create_credentials
from uesp.web.clients.site import Site, create_site
from uesp.web.wiki.edit import EditResponse
from uesp.web.wiki.login import LoginResponse
from uesp.web.wiki.status import EditResult, LoginStatus


def main() -> None:
    """
    Main entry point for this application.
    """

    environment:str|None = os.environ.get("ENVIRONMENT")
    if not environment:
        print("No environment specified. Please set the 'ENVIRONMENT' variable in the `.env` file.")
        return

    site:Site = create_site("configuration.site.json", environment)
    credential:Credential = create_credentials()
    client:Client = Client(site)

    try:
        loginResponse:LoginResponse = client.login(credential.username, credential.password)
    except Exception as exception:
        print(f"Login failed with exception: {exception}")
        return

    if loginResponse.status_code != HTTPStatus.OK:
        print(f"HTTP request failed: '{loginResponse.status_code}'")
        return
    elif loginResponse.status != LoginStatus.PASS:
        print(f"Login failed: '{loginResponse.status}'")
        return
    else:
        print(f"Login successfull for '{credential.username}'.")


    # Begin making page edits

    client.edit("User:Scrivener07", "My name is Scrivener and I have been modding since TES4 Oblivion.", "This is a test edit made by Scrivener07's bot." )

    response:EditResponse = client.edit("User:Scrivener07/Bot", "This is a test edit made by Scrivener07's bot.", "This is a test edit that uses the API." )
    if response.status_code == HTTPStatus.OK:
        print("Edit request was successful.")
    else:
        print(f"Edit request failed with status code: {response.status_code}")
        return

    if response.result == EditResult.SUCCESS:
        print("Edit was successful.")
    else:
        print(f"Edit failed with result: {response.result}")
        return

    if response.revision:
        print(f"Edit successful! New revision ID: {response.revision}")
    else:
        print(f"No new revision ID returned: {response.revision}")
