from http import HTTPStatus
from typing import Any
from requests import Response, Session
from scribe.web.configuration import Site
from scribe.web.api.edit import EditParameters, EditResponse
from scribe.web.api.login import LoginParameters, LoginResponse, TokenResponse, TokenParameters, TokenType
from scribe.web.api.status import LoginStatus


class Client:
    """Handles authenticated MediaWiki API sessions."""

    def __init__(self, site:Site) -> None:
        self.site:Site = site
        self.session:Session = Session()
        self.username:str|None = None
        self.logged_in:bool = False
        self.csrf_token:str|None = None


    # Login
    #--------------------------------------------------

    def login(self, username:str|None, password:str|None) -> LoginResponse:
        if not username or not password:
            raise Exception("Username and password must be provided")

        login_token:str|None = self._get_login_token()
        if not login_token:
            raise Exception("Failed to get login token")

        parameters:LoginParameters = LoginParameters()
        parameters.username = username
        parameters.password = password
        parameters.login_token = login_token
        parameters.login_return_url = self.site.Article
        arguments:Any = parameters.arguments()

        response:Response = self.session.post(self.site.API, data=arguments)
        loginResponse:LoginResponse = LoginResponse(response)

        if loginResponse.status_code == HTTPStatus.OK and loginResponse.status == LoginStatus.PASS:
            self.username = username
            self.logged_in = True
        return loginResponse


    def _get_login_token(self) -> str | None:
        """Get login token for authentication."""
        parameters:TokenParameters = TokenParameters()
        parameters.type = TokenType.LOGIN
        arguments:Any = parameters.arguments()
        response:Response = self.session.get(self.site.API, params=arguments)
        tokenResponse:TokenResponse = TokenResponse(response)
        return tokenResponse.login


    # Editing
    #--------------------------------------------------

    def _get_csrf_token(self) -> str | None:
        """Get CSRF token for editing."""
        if not self.logged_in:
            raise Exception("Must be logged in to get CSRF token")

        parameters:TokenParameters = TokenParameters()
        parameters.type = TokenType.CSRF
        arguments:Any = parameters.arguments()
        response:Response = self.session.get(self.site.API, params=arguments)
        tokenResponse:TokenResponse = TokenResponse(response)
        if tokenResponse.status_code == HTTPStatus.OK:
            self.csrf_token = tokenResponse.csrf
            return tokenResponse.csrf
        else:
            raise Exception(f"HTTP request for CSRF token failed. Status code: {tokenResponse.status_code}")


    def edit(self, title:str, text:str, summary:str) -> EditResponse:
        if not self.logged_in:
            raise Exception("Must be logged in to edit pages.")

        # Get CSRF token if we don't have one
        if not self.csrf_token:
            if not self._get_csrf_token():
                raise Exception("Failed to get CSRF token.")

        # Create the edit parameters
        parameters:EditParameters = EditParameters()
        parameters.title = title
        parameters.text = text
        parameters.summary = summary
        parameters.token = self.csrf_token
        parameters.bot = True
        arguments:dict[str, str] = parameters.to_arguments()

        # Post the edit request
        response:Response = self.session.post(self.site.API, data=arguments)
        return EditResponse(response)
