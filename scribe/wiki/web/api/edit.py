"""
Provides the MediaWiki `edit` API.
	Help:
        - https://www.mediawiki.org/wiki/API:Edit
        - https://www.mediawiki.org/w/api.php?action=help&modules=edit
"""
from typing import Any
from requests import Response
from scribe.wiki.web.api.actions import Action
from scribe.wiki.web.api.parameters import ParameterType
from scribe.wiki.web.api.responses import ResponseType
from scribe.wiki.web.api.status import DataFormat, EditResult


class EditParameters(ParameterType):
    def __init__(self) -> None:
        self.title:str = ""
        """The title of the page to edit. Required."""
        self.text:str = ""
        """The new text of the page."""
        self.summary:str = ""
        """The edit summary."""
        self.token:str|None = None
        """CSRF token for authentication. Required."""
        self.format:DataFormat = DataFormat.JSON
        """Format of the response data. Default is JSON."""
        self.bot:bool = True
        """Marks this as a bot edit. Ignored unless user account has bot rights."""


    def to_arguments(self) -> dict[str, str]:
        arguments:dict[str, str] = {}
        arguments["action"] = Action.EDIT
        arguments["title"] = self.title
        arguments["text"] = self.text
        arguments["summary"] = self.summary
        if self.token:
            arguments["token"] = self.token
        arguments["format"] = self.format.value
        if self.bot:
            arguments["bot"] = "true"
        return arguments


class EditResponse(ResponseType):
    def __init__(self, response:Response) -> None:
        super().__init__(response)

        data:dict[str, Any] = response.json()
        edit:dict[str, Any] = data.get("edit", {})

        self.result:EditResult|None = EditResult(edit["result"])
        """The result of the edit operation. Typically 'Success'."""

        self.page_id:int|None = edit.get("pageid")
        """The ID of the page that was edited."""

        self.title:str|None = edit.get("title")
        """The title of the page that was edited."""

        self.revision:int|None = edit.get("newrevid")
        """The new revision ID after the edit."""
