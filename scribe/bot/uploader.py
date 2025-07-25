from http import HTTPStatus
import os
from scribe.web import _api
from scribe.web.client import Client
from scribe.web.credentials import Credential, create_credentials
from scribe.web.configuration import Site, create_site
from scribe.web.api.edit import EditResponse
from scribe.web.api.login import LoginResponse
from scribe.web.api.status import EditResult, LoginStatus


def save_to_file(content:str, filename:str) -> None:
    folder:str = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


# directory: "./output"
def save_api(site:Site, directory:str) -> None:
    print("Probing MediaWiki API capabilities...")

    output_file_info:str = directory + "/siteinfo.json"
    output_file_help:str = directory + "/api_help.html"
    output_file_modules:str = directory + "/api_modules.json"
    output_file_query:str = directory + "/query_modules.json"

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created output folder: {directory}")

    if not os.path.exists(output_file_info):
        dump_info:str = _api.info(site)
        save_to_file(dump_info, output_file_info)
        print(f"Site info saved to {output_file_info}")

    if not os.path.exists(output_file_help):
        dump_help:str = _api.help(site)
        save_to_file(dump_help, output_file_help)
        print(f"API help saved to {output_file_help}")

    if not os.path.exists(output_file_modules):
        dump_modules:str = _api.modules(site)
        save_to_file(dump_modules, output_file_modules)
        print(f"API modules info saved to {output_file_modules}")

    if not os.path.exists(output_file_query):
        dump_modules_query:str = _api.modules_query(site)
        save_to_file(dump_modules_query, output_file_query)
        print(f"Query modules info saved to {output_file_query}")



def start() -> None:
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
