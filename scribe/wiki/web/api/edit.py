"""
Provides the MediaWiki `edit` API.

Documentation:
    - https://www.mediawiki.org/wiki/API:Edit
    - https://www.mediawiki.org/w/api.php?action=help&modules=edit
"""
from enum import Enum
from requests import Response
from scribe.wiki.web.api.actions import Action
from scribe.wiki.web.api.data import DataFormat, DataBoolean
from scribe.wiki.web.api.main import Main
from scribe.wiki.web.api.responses import ResponseType
from scribe.wiki.web.api.types import EditResult

class Edit(str, Enum):
    """
    Parameters for the MediaWiki edit API.
    Other general parameters are available.

    Help:
    - https://www.mediawiki.org/w/api.php?action=help&modules=edit
    """

    @staticmethod
    def _get_data(title:str, text:str, summary:str, token:str|None, bot:bool=False) -> dict[str, str]:
        data:dict[str, str] = {}
        data[Main.ACTION] = Action.EDIT
        data[Main.FORMAT] = DataFormat.JSON_FM
        data[Edit.TITLE] = title
        data[Edit.TEXT] = text
        data[Edit.SUMMARY] = summary
        if token:
            data[Edit.TOKEN] = token
        if bot:
            data[Edit.BOT] = DataBoolean.TRUE
        return data


    TITLE = "title"
    """
    Title of the page to edit. Cannot be used together with `pageid`.
    """

    PAGE_ID = "pageid"
    """
    Page ID of the page to edit. Cannot be used together with `title`.

    Type: integer
    """

    SECTION = "section"
    """
    Section identifier.

    Is `0` for the top section, `new` for a new section.
    Often a positive integer, but can also be non-numeric.
    """

    SECTION_TITLE = "sectiontitle"
    """
    The title for a new section when using `section=new`.
    """

    TEXT = "text"
    """
    Page content.
    """

    SUMMARY = "summary"
    """
    Edit summary.
    When this parameter is not provided or empty, *an edit summary may be generated automatically*.

    See: *autosummary* (https://www.mediawiki.org/wiki/Special:MyLanguage/Autosummary)

    When using `section=new` and `sectiontitle` is not provided, the value of this parameter is used for the section title instead, and an edit summary is generated automatically.
    """

    TAGS = "tags"
    """
    Change tags to apply to the revision.

    Values (separate with | or *alternative*): AWB, convenient-discussions

    See: *alternative* (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatypes)
    """

    MINOR = "minor"
    """
    Mark this edit as a minor edit.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    NOT_MINOR = "notminor"
    """
    Do not mark this edit as a minor edit even if the "Mark all edits minor by default" user preference is set.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    BOT = "bot"
    """
    Mark this edit as a bot edit.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    BASE_REV_ID = "baserevid"
    """
    ID of the base revision, used to detect edit conflicts.
    May be obtained through `action=query&prop=revisions` (https://www.mediawiki.org/w/api.php?action=help&modules=query%2Brevisions).
    Self-conflicts cause the edit to fail unless `basetimestamp` is set.

    Type: integer
    """

    BASE_TIME_STAMP = "basetimestamp"
    """
    Timestamp of the base revision, used to detect edit conflicts.
    May be obtained through `action=query&prop=revisions&rvprop=timestamp` (https://www.mediawiki.org/w/api.php?action=help&modules=query%2Brevisions).
    Self-conflicts are ignored.

    Type: `timestamp` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/timestamp)
    """

    START_TIME_STAMP = "starttimestamp"
    """
    Timestamp when the editing process began, used to detect edit conflicts.
    An appropriate value may be obtained using `curtimestamp` when beginning the edit process (e.g. when loading the page content to edit).

    See: `curtimestamp` (https://www.mediawiki.org/w/api.php?action=help&modules=main)

    Type: `timestamp` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/timestamp)
    """

    RECREATE = "recreate"
    """
    Override any errors about the page having been deleted in the meantime.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    CREATE_ONLY = "createonly"
    """
    Don't edit the page if it exists already.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    NO_CREATE = "nocreate"
    """
    Throw an error if the page doesn't exist.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    WATCH = "watch"
    """
    Deprecated.
    Add the page to the current user's watchlist.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    UNWATCH = "unwatch"
    """
    Deprecated.
    Remove the page from the current user's watchlist.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    WATCHLIST = "watchlist"
    """
    Unconditionally add or remove the page from the current user's watchlist, use preferences (ignored for bot users) or do not change watch.

    One of the following values: `nochange`, `preferences`, `unwatch`, `watch`

    Default: `preferences`
    """

    WATCHLIST_EXPIRY = "watchlistexpiry"
    """
    Watchlist expiry `timestamp`.
    Omit this parameter entirely to leave the current expiry unchanged.

    Type: `expiry` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/expiry)
    """

    MD5 = "md5"
    """
    The MD5 hash of the `text` parameter, or the `prependtext` and `appendtext` parameters concatenated.
    If set, the edit won't be done unless the hash is correct.
    """

    PREPEND_TEXT = "prependtext"
    """
    Add this text to the beginning of the page or section.

    Overrides text.
    """

    APPEND_TEXT = "appendtext"
    """
    Add this text to the end of the page or section.

    Overrides text.

    Use `section=new` to append a new section, rather than this parameter.
    """

    UNDO = "undo"
    """
    Undo this revision.
    Overrides `text`, `prependtext` and `appendtext`.

    Type: `integer` The value must be no less than 0.
    """

    UNDO_AFTER = "undoafter"
    """
    Undo all revisions from undo to this one.
    If not set, just undo one revision.

    Type: `integer` The value must be no less than 0.
    """

    REDIRECT = "redirect"
    """
    Automatically resolve redirects.

    Type: `boolean` (https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean)
    """

    CONTENT_FORMAT = "contentformat"
    """
    Content serialization format used for the input text.

    One of the following values:
    - `application/json`
    - `application/octet-stream`
    - `application/unknown`
    - `application/vue+xml`
    - `application/x-binary`
    - `text/css`
    - `text/javascript`
    - `text/plain`
    - `text/unknown`
    - `text/x-wiki`
    - `unknown/unknown`
    """

    CONTENT_MODEL = "contentmodel"
    """
    Content model of the new content.

    One of the following values:
    - `GadgetDefinition`
    - `Graph.JsonConfig`
    - `Json.JsonConfig`
    - `JsonSchema`
    - `MassMessageListContent`
    - `NewsletterContent`
    - `Scribunto`
    - `SecurePoll`
    - `css`
    - `flow-board`
    - `javascript`
    - `json`
    - `sanitized-css`
    - `text`
    - `translate-messagebundle`
    - `unknown`
    - `vue`
    - `wikitext`
    """

    TOKEN = "token"
    """
    A "csrf" token retrieved from `action=query&meta=tokens`.

    The token should always be sent as the last parameter, or at least after the `text` parameter.

    This parameter is required.
    """

    RETURN_TO = "returnto"
    """
    Page title.
    If saving the edit created a temporary account, the API may respond with an URL that the client should visit to complete logging in.
    If this parameter is provided, the URL will redirect to the given page, instead of the page that was edited.

    Type: `page title` Accepts non-existent pages.
    """

    RETURN_TO_QUERY = "returntoquery"
    """
    URL query parameters (with leading ?).
    If saving the edit created a temporary account, the API may respond with an URL that the client should visit to complete logging in.
    If this parameter is provided, the URL will redirect to a page with the given query parameters.

    Default: (empty)
    """

    RETURN_TO_ANCHOR = "returntoanchor"
    """
    URL fragment (with leading #).
    If saving the edit created a temporary account, the API may respond with an URL that the client should visit to complete logging in.
    If this parameter is provided, the URL will redirect to a page with the given fragment.

    Default: (empty)
    """

    CAPTCHA_WORD = "captchaword"
    """
    Answer to the CAPTCHA.
    """

    CAPTCHA_ID = "captchaid"
    """
    CAPTCHA ID from previous request.
    """


class EditResponseType(str, Enum):
    RESULT = "result"
    PAGE_ID = "pageid"
    TITLE = "title"
    NEW_REV_ID = "newrevid"


class EditResponse(ResponseType):
    ATTRIBUTE_CONTENT_MODEL:str = "contentmodel"
    ATTRIBUTE_NO_CHANGE:str = "nochange"
    ATTRIBUTE_WATCHED:str = "watched"

    def __init__(self, response:Response) -> None:
        super().__init__(response)

        self.result:EditResult|None = None
        """The result of the edit operation. Typically 'Success'."""

        self.page_id:int|None = None
        """The ID of the page that was edited."""

        self.title:str|None = None
        """The title of the page that was edited."""

        self.revision:int|None = None
        """The new revision ID after the edit."""
