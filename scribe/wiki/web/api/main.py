"""
https://www.mediawiki.org/wiki/API:Main_page
"""
from enum import Enum

class Main(str, Enum):
    ACTION = "action"
    """
    Which action to perform.

    Default: `help`
    """

    FORMAT = "format"
    """
    The format of the output.

    One of the following values:
    - `json`: https://www.mediawiki.org/w/api.php?action=help&modules=json
    - `jsonfm`: https://www.mediawiki.org/w/api.php?action=help&modules=jsonfm
    - `none`: https://www.mediawiki.org/w/api.php?action=help&modules=none
    - `php`: https://www.mediawiki.org/w/api.php?action=help&modules=php
    - `phpfm`: https://www.mediawiki.org/w/api.php?action=help&modules=phpfm
    - `rawfm`: https://www.mediawiki.org/w/api.php?action=help&modules=rawfm
    - `xml`: https://www.mediawiki.org/w/api.php?action=help&modules=xml
    - `xmlfm`: https://www.mediawiki.org/w/api.php?action=help&modules=xmlfm

    Default: `jsonfm`
    """

    MAX_LAG = "maxlag"
    """
    Maximum lag can be used when MediaWiki is installed on a database replicated cluster.

    To save actions causing any more site replication lag, this parameter can make the client wait until the replication lag is less than the specified value.
    In case of excessive lag, error code `maxlag` is returned with a message like `Waiting for $host: $lag seconds lagged`.

    See Manual: Maxlag parameter for more information.
    https://www.mediawiki.org/wiki/Special:MyLanguage/Manual:Maxlag_parameter

    Type: `integer`
    """

    SMAX_AGE = "smaxage"
    """
    Set the `s-maxag`e HTTP cache control header to this many seconds.
    Errors are never cached.

    Type: `integer` (The value must be no less than 0.)

    Default: `0`
    """

    MAX_AGE = "maxage"
    """
    Set the `max-age` HTTP cache control header to this many seconds.
    Errors are never cached.

    Type: integer (The value must be no less than 0.)

    Default: 0
    """

    ASSERT = "assert"
    """
    Verify that the user is logged in (including possibly as a temporary user) if set to `user`,
    not logged in if set to `anon`,
    or has the bot user right if `bot`.

    One of the following values: `anon`, `bot`, `user`
    """

    ASSERT_USER = "assertuser"
    """
    Verify the current user is the named user.

    Type: `user`, by any of username and Temporary user
    """

    REQUEST_ID = "requestid"
    """
    Any value given here will be included in the response.
    May be used to distinguish requests.
    """

    SERVED_BY = "servedby"
    """
    Include the hostname that served the request in the results

    Type: boolean (details)
    """

    CUR_TIME_STAMP = "curtimestamp"
    """
    Include the current timestamp in the result.

    Type: boolean (details)
    """

    RESPONSE_LANG_INFO = "responselanginfo"
    """
    Include the languages used for `uselang` and `errorlang` in the result.

    Type: boolean (details)
    """

    ORIGIN = "origin"
    """
    When accessing the API using a cross-domain AJAX request (CORS), set this to the originating domain.
    This must be included in any pre-flight request, and therefore must be part of the request URI (not the POST body).

    For authenticated requests, this must match one of the origins in the `Origin` header exactly, so it has to be set to something like https://en.wikipedia.org or https://meta.wikimedia.org.
    If this parameter does not match the `Origin` header, a 403 response will be returned.
    If this parameter matches the `Origin` header and the origin is allowed, the `Access-Control-Allow-Origin` and` Access-Control-Allow-Credentials` headers will be set.

    For non-authenticated requests, specify the value `*`.
    This will cause the `Access-Control-Allow-Origin` header to be set, but `Access-Control-Allow-Credentials` will be `false` and all user-specific data will be restricted.
    """

    CROSS_ORIGIN = "crossorigin"
    """
    When accessing the API using a cross-domain AJAX request (CORS) and using a session provider that is safe against cross-site request forgery (CSRF) attacks (such as OAuth),
    use this instead of `origin=*` to make the request authenticated (i.e., not logged out).
    This must be included in any pre-flight request, and therefore must be part of the request URI (not the POST body).

    Note that most session providers, including standard cookie-based sessions, do not support authenticated CORS and cannot be used with this parameter.

    Type: boolean (details)
    """

    USE_LANG = "uselang"
    """
    Language to use for message translations.
    `action=query&meta=siteinfo&siprop=languages` returns a list of language codes.
    You can specify `user` to use the current user's language preference or `content` to use this wiki's content language.

    Default: `user`
    """

    VARIANT = "variant"
    """
    Variant of the language.
    Only works if the base language supports variant conversion.
    """

    ERROR_FORMAT = "errorformat"
    """
    Format to use for warning and error text output
    - `plaintext`: Wikitext with HTML tags removed and entities replaced.
    - `wikitext`: Unparsed wikitext.
    - `html`: HTML
    - `raw`: Message key and parameters.
    - `none`: No text output, only the error codes.
    - `bc`: Format used prior to MediaWiki 1.29. `errorlang` and `errorsuselocal` are ignored.

    One of the following values: `bc`, `html`, `none`, `plaintext`, `raw`, `wikitext`

    Default: `bc`
    """

    ERROR_LANG = "errorlang"
    """
    Language to use for warnings and errors.
    `action=query&meta=siteinfo&siprop=languages` returns a list of language codes.
    Specify `content` to use this wiki's content language or `uselang` to use the same value as the `uselang` parameter.

    Default: `uselang`
    """

    ERRORS_USE_LOCAL = "errorsuselocal"
    """
    If given, error texts will use locally-customized messages from the MediaWiki namespace.

    Type: boolean (details)
    """

    CENTRAL_AUTH_TOKEN = "centralauthtoken"
    """
    When accessing the API using a cross-domain AJAX request (CORS), use this to authenticate as the current SUL user.

    Use `action=centralauthtoken` on this wiki to retrieve the token, before making the CORS request.
    Each token may only be used once, and expires after 10 seconds.
    This should be included in any pre-flight request, and therefore should be included in the request URI (not the POST body).
    """
