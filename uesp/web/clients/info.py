import os
from uesp.web.clients import api
from uesp.web.clients.site import Site


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
        dump_info:str = api.info(site)
        save_to_file(dump_info, output_file_info)
        print(f"Site info saved to {output_file_info}")

    if not os.path.exists(output_file_help):
        dump_help:str = api.help(site)
        save_to_file(dump_help, output_file_help)
        print(f"API help saved to {output_file_help}")

    if not os.path.exists(output_file_modules):
        dump_modules:str = api.modules(site)
        save_to_file(dump_modules, output_file_modules)
        print(f"API modules info saved to {output_file_modules}")

    if not os.path.exists(output_file_query):
        dump_modules_query:str = api.modules_query(site)
        save_to_file(dump_modules_query, output_file_query)
        print(f"Query modules info saved to {output_file_query}")
