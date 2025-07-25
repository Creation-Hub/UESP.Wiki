from requests import Response

class ResponseType:
    def __init__(self, response:Response) -> None:
        self.response:Response = response
        """The original HTTP response object."""

    @property
    def status_code(self) -> int:
        """Returns the HTTP status code of the response."""
        return self.response.status_code

    @property
    def ok(self) -> bool:
        """Returns True if the HTTP response status code is 200-299."""
        return self.response.ok
