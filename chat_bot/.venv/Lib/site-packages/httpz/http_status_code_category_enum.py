import enum


class HTTPStatusCodeCategoryEnum(enum.Enum):
    """ HTTP Response Status Code enum """

    INFORMATIONAL = "informational"
    SUCCESSFUL = "successful"
    REDIRECTION = "redirection"
    CLIENT_ERROR = "client_error"
    SERVER_ERROR = "server_error"

    @classmethod
    def to_list(cls):
        return [i.value for i in cls]
