"""
Provides the MediaWiki `login` API.
	Help:
        - https://www.mediawiki.org/wiki/API:Login
        - https://www.mediawiki.org/w/api.php?action=help&modules=login
        - https://www.mediawiki.org/w/api.php?action=help&modules=clientlogin
        - https://www.mediawiki.org/wiki/API:Query
        - https://www.mediawiki.org/wiki/API:Query#Example_5:_Batchcomplete
"""
from enum import Enum
from typing import Any
from requests import Response
from scribe.wiki.web.api.actions import Action
from scribe.wiki.web.api.parameters import ParameterType
from scribe.wiki.web.api.responses import ResponseType
from scribe.wiki.web.api.status import DataFormat


# Login
#--------------------------------------------------

class LoginParameters(ParameterType):
    """Parameters for the MediaWiki login API."""
    def __init__(self) -> None:
        super().__init__()

        self.username:str = ""
        """The username to log in with. Required."""

        self.password:str = ""
        """The password to log in with. Required."""

        self.login_token:str = ""
        """The login token for authentication. Required."""

        self.login_return_url:str = ""
        """The URL to redirect to after login. Optional."""

        self.format:DataFormat = DataFormat.JSON
        """The format of the response data. Default is JSON."""


    def arguments(self) -> dict[str, str]:
        """Gets a dictionary of API request arguments."""
        arguments:dict[str, str] = {}
        arguments["action"] = Action.CLIENTLOGIN
        arguments["username"] = self.username
        arguments["password"] = self.password
        arguments["logintoken"] = self.login_token
        arguments["loginreturnurl"] = self.login_return_url
        arguments["format"] = self.format
        return arguments


class LoginResponse(ResponseType):
    """Response from the MediaWiki login API."""
    def __init__(self, response:Response) -> None:
        super().__init__(response)
        data:dict[str, Any] = response.json()
        login:dict[str, Any] = data.get("clientlogin", {})
        self.status:str|None = login.get("status")
        """The status of the login operation."""


# Token
#--------------------------------------------------

class TokenType(str, Enum):
    """Enumeration of token types for MediaWiki API."""
    LOGIN = "login"
    CSRF = "csrf"


class TokenParameters(ParameterType):
    """Parameters for retrieving tokens from the MediaWiki API."""

    def __init__(self) -> None:
        super().__init__()

        self.action:Action = Action.QUERY
        """The action to perform."""

        self.meta:str = "tokens"
        """The meta parameter to request tokens."""

        self.type:str = TokenType.LOGIN
        """The "login" or empty for CSRF token."""

        self.format:DataFormat = DataFormat.JSON
        """The format of the response data."""


    def arguments(self) -> dict[str, str]:
        """Gets a dictionary of API request arguments."""
        arguments:dict[str, str] = {}
        arguments["action"] = self.action
        arguments["meta"] = self.meta
        arguments["type"] = self.type
        arguments["format"] = self.format
        return arguments


class TokenResponse(ResponseType):
    def __init__(self, response:Response) -> None:
        super().__init__(response)
        data:dict[str, Any] = response.json()
        query:dict[str, Any] = data.get("query", {})
        self.tokens:dict[str, Any] = query.get("tokens", {})
        """The tokens dictionary containing login and csrf tokens."""

    @property
    def login(self) -> str | None:
        return self.tokens.get("logintoken")

    @property
    def csrf(self) -> str | None:
        return self.tokens.get("csrftoken")

    def get(self, type:TokenType) -> str | None:
        """Get any token type dynamically"""
        types:dict[TokenType, str] = {
            TokenType.LOGIN: "logintoken",
            TokenType.CSRF: "csrftoken"
        }
        key:str|None = types.get(type)
        return self.tokens.get(key) if key else None
