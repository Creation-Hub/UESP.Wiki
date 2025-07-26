from http import HTTPStatus
import logging
import os
from scribe.app.context import AppContext
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
    logging.info("Probing MediaWiki API capabilities...")

    output_file_info:str = directory + "/siteinfo.json"
    output_file_help:str = directory + "/api_help.html"
    output_file_modules:str = directory + "/api_modules.json"
    output_file_query:str = directory + "/query_modules.json"

    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created output folder: {directory}")

    if not os.path.exists(output_file_info):
        dump_info:str = _api.info(site)
        save_to_file(dump_info, output_file_info)
        logging.info(f"Site info saved to {output_file_info}")

    if not os.path.exists(output_file_help):
        dump_help:str = _api.help(site)
        save_to_file(dump_help, output_file_help)
        logging.info(f"API help saved to {output_file_help}")

    if not os.path.exists(output_file_modules):
        dump_modules:str = _api.modules(site)
        save_to_file(dump_modules, output_file_modules)
        logging.info(f"API modules info saved to {output_file_modules}")

    if not os.path.exists(output_file_query):
        dump_modules_query:str = _api.modules_query(site)
        save_to_file(dump_modules_query, output_file_query)
        logging.info(f"Query modules info saved to {output_file_query}")



def start(app:AppContext) -> None:
    if not app.settings.environment:
        logging.error("No environment specified.")
        return

    site:Site = create_site("configuration.site.json", app.settings.environment)
    credential:Credential = create_credentials()
    client:Client = Client(site)

    try:
        loginResponse:LoginResponse = client.login(credential.username, credential.password)
    except Exception as exception:
        logging.error(f"Login failed with exception: {exception}")
        return

    if loginResponse.status_code != HTTPStatus.OK:
        logging.error(f"HTTP request failed: '{loginResponse.status_code}'")
        return
    elif loginResponse.status != LoginStatus.PASS:
        logging.error(f"Login failed: '{loginResponse.status}'")
        return
    else:
        logging.error(f"Login successfull for '{credential.username}'.")


    # Begin making page edits

    client.edit("User:Scrivener07", "My name is Scrivener and I have been modding since TES4 Oblivion.", "This is a test edit made by Scrivener07's bot." )

    response:EditResponse = client.edit("User:Scrivener07/Bot", "This is a test edit made by Scrivener07's bot.", "This is a test edit that uses the API." )
    if response.status_code == HTTPStatus.OK:
        logging.info("Edit request was successful.")
    else:
        logging.error(f"Edit request failed with status code: {response.status_code}")
        return

    if response.result == EditResult.SUCCESS:
        logging.info("Edit was successful.")
    else:
        logging.error(f"Edit failed with result: {response.result}")
        return

    if response.revision:
        logging.info(f"Edit successful! New revision ID: {response.revision}")
    else:
        logging.warning(f"No new revision ID returned: {response.response.content}")
