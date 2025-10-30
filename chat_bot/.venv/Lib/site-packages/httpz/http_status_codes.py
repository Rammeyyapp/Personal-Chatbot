from typing import Union, List, Dict

from httpz.http_status_code import HTTPStatusCode
from httpz.status_codes import (status_codes, informational, successful,
                                redirection, client_error, server_error)

category_map: Dict[str, Dict] = {
    "informational": informational,
    "successful": successful,
    "redirection": redirection,
    "client_error": client_error,
    "server_error": server_error,
}


class HTTPStatusCodes(object):
    """ HTTP status code factory """

    @staticmethod
    def get(code: Union[str, int]) -> HTTPStatusCode:
        """ Returns an HTTPStatusCode object

        >>> HTTPStatusCodes.get("200")
        HTTPStatusCode(code=200, message=OK, description=The request has succeeded)

        Args:
            code: Union[int, str] = HTTP Status code
        Returns:
            HTTPStatusCode
        Raises:
            KeyError if the code is not found
        """

        return HTTPStatusCode(**status_codes[str(code)])

    @staticmethod
    def get_category(category: str) -> List[HTTPStatusCode]:
        """ Returns all status code objects in a category """

        return [HTTPStatusCode(**v) for k, v in category_map[category].items()]

    @staticmethod
    def get_all() -> List[HTTPStatusCode]:
        """ Returns all HTTPStatusCode objects """

        return [HTTPStatusCode(**v) for k, v in status_codes.items()]
