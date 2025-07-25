import os

class Credential():
    def __init__(self, username:str|None, password:str|None) -> None:
        self.username:str|None = username
        self.password:str|None = password

def create_credentials() -> Credential:
    """Get wiki credentials from environment variables."""
    username:str|None = os.environ.get('WIKI_USERNAME')
    password:str|None = os.environ.get('WIKI_PASSWORD')
    return Credential(username, password)
