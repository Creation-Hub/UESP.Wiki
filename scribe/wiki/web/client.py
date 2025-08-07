from http import HTTPStatus
import json
from typing import Any
from requests import Response, Session
from scribe.wiki.web.api.actions import Action
from scribe.wiki.web.api.data import DataBoolean, DataFormat
from scribe.wiki.web.api.edit import Edit
from scribe.wiki.web.api.errors import ErrorType, ResponseError
from scribe.wiki.web.api.main import Main
from scribe.wiki.web.site import Site
from scribe.wiki.web.api.edit import EditResponse, EditResponseType
from scribe.wiki.web.api.login import LoginParameters, LoginResponse, TokenResponse, TokenParameters, TokenType
from scribe.wiki.web.api.types import EditResult, LoginStatus

class WebClient:
    """Handles authenticated MediaWiki API sessions."""


    # TODO: I think I messed up the edit parameter json structure shape.
    # The response header content type we are getting is `Content-Type: text/html; charset=UTF-8`.
    # This is likely because the API is returning an HTML error page instead of JSON.
    # ---> Unexpected content type in response: `text/html; charset=UTF-8`. Expected `application/json`.
    RESPONSE_CONTENT_TYPE_JSON:str = "application/json"
    RESPONSE_CONTENT_TYPE_HTML:str = "text/html"


    def __init__(self, site:Site) -> None:
        super().__init__()
        self.site:Site = site
        self.session:Session = Session()
        self.username:str|None = None
        self.logged_in:bool = False
        self.csrf_token:str|None = None


    # Authentication
    #--------------------------------------------------

    def _get_login_token(self) -> str | None:
        """Gets an authentication login token by GET request."""
        parameters:TokenParameters = TokenParameters()
        parameters.type = TokenType.LOGIN
        arguments:Any = parameters.arguments()
        response:Response = self.session.get(self.site.api_url, params=arguments)
        tokenResponse:TokenResponse = TokenResponse(response)
        return tokenResponse.login


    def _get_csrf_token(self) -> str | None:
        """Gets an editing authentication CSRF token by GET request."""
        if not self.logged_in:
            raise Exception("Must be logged in to get CSRF token")

        parameters:TokenParameters = TokenParameters()
        parameters.type = TokenType.CSRF
        arguments:Any = parameters.arguments()
        response:Response = self.session.get(self.site.api_url, params=arguments)
        tokenResponse:TokenResponse = TokenResponse(response)
        if tokenResponse.status_code == HTTPStatus.OK:
            self.csrf_token = tokenResponse.csrf
            return tokenResponse.csrf
        else:
            raise Exception(f"HTTP request for CSRF token failed. Status code: {tokenResponse.status_code}")


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
        parameters.login_return_url = self.site.article_url
        arguments:Any = parameters.arguments()

        response:Response = self.session.post(self.site.api_url, data=arguments)
        loginResponse:LoginResponse = LoginResponse(response)

        if loginResponse.status_code == HTTPStatus.OK and loginResponse.status == LoginStatus.PASS:
            self.username = username
            self.logged_in = True
        return loginResponse


    def logout(self) -> None:
        """Logs out the current user."""
        raise NotImplementedError("Logout functionality is not implemented yet.")


    # Editing
    #--------------------------------------------------

    # TODO: This is a huge mess.
    def edit(self, title:str, text:str, summary:str) -> EditResponse:
        if not self.logged_in:
            raise Exception("Must be logged in to edit pages.")

        # Get CSRF token if we don't have one.
        if not self.csrf_token:
            if not self._get_csrf_token():
                raise Exception("Failed to get CSRF token.")
        # TODO: This is too funky.
        if not self.csrf_token:
            raise Exception("Failed to get CSRF token.")

        # Create the edit POST request data parameters.
        post_data:dict[str, str] = {}
        post_data[Main.ACTION] = Action.EDIT
        post_data[Main.FORMAT] = DataFormat.JSON # Using JSON_FM breaks the post call.
        post_data[Edit.TITLE] = title
        post_data[Edit.TEXT] = text
        post_data[Edit.SUMMARY] = summary
        post_data[Edit.TOKEN] = self.csrf_token
        post_data[Edit.BOT] = DataBoolean.TRUE

        # TODO: These are for temporary debugging.
        # post_data[EditParameter.CONTENT_MODEL] = 'wikitext'
        # post_data[EditParameter.CONTENT_FORMAT] = 'json'

        # Post edit request with this client session.
        response:Response = self.session.post(self.site.api_url, data=post_data)

        # Debug the raw response.
        # logging.debug(f"response.status_code: {response.status_code}")
        # logging.debug(f"response.headers: ...\n{response.headers}")
        # logging.debug(f"response.text: ...\n{response.text[:500]}...")

        if not response.text.strip():
            raise Exception(f"Empty response from MediaWiki API. Status: {response.status_code}")


        response_content_type:str = response.headers.get("Content-Type", "")
        if WebClient.RESPONSE_CONTENT_TYPE_JSON not in response_content_type:
            raise Exception(f"Unexpected content type in response: `{response_content_type}`. Expected `{WebClient.RESPONSE_CONTENT_TYPE_JSON}`.")

        try:
            response_data = response.json()
        except json.JSONDecodeError as jsonDecodeError:
            raise Exception(
                f"Failed to decode JSON response. " +
                f"\nJSONDecodeError: {jsonDecodeError}" +
                f"\nStatus: {response.status_code}" +
                f"\nContent-Type: {response_content_type}" +
                f"\nResponse body: {response.text[:200]}..."
            )

        # Decode the response.
        response_data:dict[str, Any] = {}
        try:
            response_data = response.json()
        except json.JSONDecodeError as jsonDecodeError:
            raise Exception(f"Failed to decode JSON response.", f"JSONDecodeError: {jsonDecodeError}", f"post_data: {post_data}", f"Response: {response}")

        # TODO: WIP
        error_data:dict[str, Any]|None = response_data.get(ErrorType.TYPE, None)
        if error_data:
            error:ResponseError = ResponseError(response)
            error.code = error_data.get(ErrorType.CODE, None)
            error.info = error_data.get(ErrorType.INFO, None)
            error.extra = error_data.get(ErrorType.EXTRA, None)
            raise Exception(error.code, error.info, error.extra)

        # TODO: WIP
        edit_data:dict[str, Any]|None = response_data.get(Action.EDIT, None)
        if not edit_data:
            raise Exception("The 'edit' response did not contain 'edit' or 'error' keys.")

        this:EditResponse = EditResponse(response)
        this.result = EditResult(edit_data.get(EditResponseType.RESULT))
        this.page_id = edit_data.get(EditResponseType.PAGE_ID)
        this.title = edit_data.get(EditResponseType.TITLE)
        this.revision = edit_data.get(EditResponseType.NEW_REV_ID)

        return this
