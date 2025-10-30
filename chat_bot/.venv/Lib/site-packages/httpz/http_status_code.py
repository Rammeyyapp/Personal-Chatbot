class HTTPStatusCode(object):
    """ HTTP Status code object """

    def __init__(self,
                 code: str,
                 message: str,
                 description: str,
                 category: str,
                 webdav: bool = False,
                 deprecated: bool = False,
                 experimental: bool = False):
        self._fields = {
            "code", "message", "description", "category", "webdav",
            "deprecated", "experimental"
        }
        self._code = code
        self._message = message
        self._description = description
        self._category = category
        self._webdav = webdav
        self._deprecated = deprecated
        self._experimental = experimental

    def __repr__(self):
        return f"{self.__class__.__name__}(code={self.code}, message={self.message}, description={self.description})"

    @property
    def code(self) -> int:
        return int(self._code)

    @property
    def message(self) -> str:
        return self._message

    @property
    def description(self) -> str:
        return self._description

    @property
    def category(self) -> str:
        return self._category

    @property
    def webdav(self) -> bool:
        return self._webdav

    @property
    def deprecated(self) -> bool:
        return self._deprecated

    @property
    def experimental(self) -> bool:
        return self._experimental

    def to_dict(self) -> dict:
        return {i: getattr(self, i) for i in self._fields}
