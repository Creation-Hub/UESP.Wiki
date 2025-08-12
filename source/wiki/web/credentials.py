import os
from typing import override

class Credential():
    """Represents wiki credentials for authentication."""

    def __init__(self, username:str|None, password:str|None) -> None:
        super().__init__()
        self.username:str|None = username
        self.password:str|None = password


    @staticmethod
    def create() -> 'Credential':
        """Get wiki credentials from environment variables."""
        username:str|None = os.environ.get("WIKI_USERNAME")
        password:str|None = os.environ.get("WIKI_PASSWORD")
        return Credential(username, password)


    @override
    def __repr__(self) -> str:
        """Return a string representation of the credential. The password is masked for security."""
        return f"Credential(username={self.username}, password={"****" if self.password else None})"


    @override
    def __str__(self) -> str:
        """Return a string representation of the credential."""
        return self.__repr__()
