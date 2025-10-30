from httpz.http_status_code_category_enum import HTTPStatusCodeCategoryEnum

informational: dict = {
    "100": {
        "code": 100,
        "message": "Continue",
        "description": "This interim response indicates that everything so far is OK and that the client should continue the request, or ignore the response if the request is already finished",
        "category": HTTPStatusCodeCategoryEnum.INFORMATIONAL.value
    },
    "101": {
        "code": 101,
        "message": "Switching Protocol",
        "description": "This code is sent in response to an Upgrade request header from the client, and indicates the protocol the server is switching to",
        "category": HTTPStatusCodeCategoryEnum.INFORMATIONAL.value
    },
    "102": {
        "code": 102,
        "message": "Processing",
        "description": "This code indicates that the server has received and is processing the request, but no response is available yet",
        "category": HTTPStatusCodeCategoryEnum.INFORMATIONAL.value,
        "webdav": True,
    },
    "103": {
        "code": 103,
        "message": "Early Hints",
        "description": "This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response",
        "category": HTTPStatusCodeCategoryEnum.INFORMATIONAL.value
    }
}

successful: dict = {
    "200": {
        "code": 200,
        "message": "OK",
        "description": "The request has succeeded",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "201": {
        "code": 201,
        "message": "Created",
        "description": "The request has succeeded and a new resource has been created as a result",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "202": {
        "code": 202,
        "message": "Accepted",
        "description": "The request has been received but not yet acted upon",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "203": {
        "code": 203,
        "message": "Non-Authoritative Information",
        "description": "The returned meta-information is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "204": {
        "code": 204,
        "message": "No Content",
        "description": "There is no content to send for this request, but the headers may be useful. The user-agent may update its cached headers for this resource with the new ones",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "205": {
        "code": 205,
        "message": "Reset Content",
        "description": "Tells the user-agent to reset the document which sent this request",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "206": {
        "code": 206,
        "message": "Partial Content",
        "description": "This response code is used when the Range header is sent from the client to request only part of a resource",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value
    },
    "207": {
        "code": 207,
        "message": "Multi-Status",
        "description": "Conveys information about multiple resources, for situations where multiple status codes might be appropriate",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value,
        "webdav": True,
    },
    "208": {
        "code": 208,
        "message": "Already Reported",
        "description": "Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value,
        "webdav": True,
    },
    "226": {
        "code": 226,
        "message": "IM Used",
        "description": "The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance",
        "category": HTTPStatusCodeCategoryEnum.SUCCESSFUL.value,
        "webdav": True,
    },
}

redirection: dict = {
    "300": {
        "code": 300,
        "message": "Multiple Choice",
        "description": "The request has more than one possible response. The user-agent or user should choose one of them",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value
    },
    "301": {
        "code": 301,
        "message": "Moved Permanently",
        "description": "The URL of the requested resource has been changed permanently. The new URL is given in the response",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value
    },
    "302": {
        "code": 302,
        "message": "Found",
        "description": "This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value
    },
    "303": {
        "code": 303,
        "message": "See Other",
        "description": "The server sent this response to direct the client to get the requested resource at another URI with a GET request",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value
    },
    "304": {
        "code": 304,
        "message": "Not Modified",
        "description": "This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value
    },
    "305": {
        "code": 305,
        "message": "Use Proxy",
        "description": "Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value,
        "deprecated": True
    },
    "306": {
        "code": 306,
        "message": "Unused",
        "description": "This response code is no longer used; it is just reserved. It was used in a previous version of the HTTP/1.1 specification",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value,
    },
    "307": {
        "code": 307,
        "message": "Temporary Redirect",
        "description": "The server sends this response to direct the client to get the requested resource at another URI with same method that was used in the prior request. This has the same semantics as the 302 Found HTTP response code, with the exception that the user agent must not change the HTTP method used",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value,
    },
    "308": {
        "code": 308,
        "message": "Permanent Redirect",
        "description": "This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used",
        "category": HTTPStatusCodeCategoryEnum.REDIRECTION.value,
    },
}

client_error: dict = {
    "400": {
        "code": 400,
        "message": "Bad Request",
        "description": "The server could not understand the request due to invalid syntax",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "401": {
        "code": 401,
        "message": "Unauthorized",
        "description": "Although the HTTP standard specifies 'unauthorized', semantically this response means 'unauthenticated'. That is, the client must authenticate itself to get the requested response",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "402": {
        "code": 402,
        "message": "Payment Required",
        "description": "Although the HTTP standard specifies 'unauthorized', semantically this response means 'unauthenticated'. That is, the client must authenticate itself to get the requested response",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value,
        "experimental": True
    },
    "403": {
        "code": 403,
        "message": "Forbidden",
        "description": "The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike 401, the client's identity is known to the server",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "404": {
        "code": 404,
        "message": "Not Found",
        "description": "The server can not find the requested resource. In the browser, this means the URL is not recognized. In an API, this can also mean that the endpoint is valid but the resource itself does not exist. Servers may also send this response instead of 403 to hide the existence of a resource from an unauthorized client",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "405": {
        "code": 405,
        "message": "Method Not Allowed",
        "description": "The request method is known by the server but has been disabled and cannot be used. For example, an API may forbid DELETE-ing a resource. The two mandatory methods, GET and HEAD, must never be disabled and should not return this error code",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "406": {
        "code": 406,
        "message": "Not Acceptable",
        "description": "This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "407": {
        "code": 407,
        "message": "Proxy Authentication Required",
        "description": "This is similar to 401 but authentication is needed to be done by a proxy",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "408": {
        "code": 408,
        "message": "Request Timeout",
        "description": "This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "409": {
        "code": 409,
        "message": "Conflict",
        "description": "This response is sent when a request conflicts with the current state of the server",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "410": {
        "code": 410,
        "message": "Gone",
        "description": "This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for 'limited-time, promotional services'. APIs should not feel compelled to indicate resources that have been deleted with this status code",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "411": {
        "code": 411,
        "message": "Length Required",
        "description": "Server rejected the request because the Content-Length header field is not defined and the server requires it",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "412": {
        "code": 412,
        "message": "Precondition Failed",
        "description": "The client has indicated preconditions in its headers which the server does not meet",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "413": {
        "code": 413,
        "message": "Payload Too Large",
        "description": "Request entity is larger than limits defined by server; the server might close the connection or return an Retry-After header field",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "414": {
        "code": 414,
        "message": "URI Too Long",
        "description": "The URI requested by the client is longer than the server is willing to interpret",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "415": {
        "code": 415,
        "message": "Unsupported Media Type",
        "description": "The media format of the requested data is not supported by the server, so the server is rejecting the request",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "416": {
        "code": 416,
        "message": "Range Not Satisfiable",
        "description": "The range specified by the Range header field in the request can't be fulfilled; it's possible that the range is outside the size of the target URI's data",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "417": {
        "code": 417,
        "message": "Expectation Failed",
        "description": "This response code means the expectation indicated by the Expect request header field can't be met by the server",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "418": {
        "code": 418,
        "message": "I'm a teapot",
        "description": "The server refuses the attempt to brew coffee with a teapot",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "421": {
        "code": 421,
        "message": "Misdirected Request",
        "description": "The request was directed at a server that is not able to produce a response. This can be sent by a server that is not configured to produce responses for the combination of scheme and authority that are included in the request URI",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "422": {
        "code": 422,
        "message": "Unprocessable Entity",
        "description": "The request was well-formed but was unable to be followed due to semantic errors",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value,
        "webdav": True
    },
    "423": {
        "code": 423,
        "message": "Locked",
        "description": "The resource that is being accessed is locked",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value,
        "webdav": True
    },
    "424": {
        "code": 424,
        "message": "Failed Dependency",
        "description": "The request failed due to failure of a previous request",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value,
        "webdav": True
    },
    "425": {
        "code": 425,
        "message": "Too Early",
        "description": "Indicates that the server is unwilling to risk processing a request that might be replayed",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "426": {
        "code": 426,
        "message": "Upgrade Required",
        "description": "The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol. The server sends an Upgrade header in a 426 response to indicate the required protocol(s)",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "428": {
        "code": 428,
        "message": "Precondition Required",
        "description": "The origin server requires the request to be conditional. This response is intended to prevent the 'lost update' problem, where a client GETs a resource's state, modifies it, and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "429": {
        "code": 429,
        "message": "Too Many Requests",
        "description": "The user has sent too many requests in a given amount of time",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "431": {
        "code": 431,
        "message": "Request Header Fields Too Large",
        "description": "The server is unwilling to process the request because its header fields are too large. The request may be resubmitted after reducing the size of the request header fields",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
    "451": {
        "code": 451,
        "message": "Unavailable For Legal Reasons",
        "description": "The server is unwilling to process the request because its header fields are too large. The request may be resubmitted after reducing the size of the request header fields",
        "category": HTTPStatusCodeCategoryEnum.CLIENT_ERROR.value
    },
}

server_error: dict = {
    "500": {
        "code": 500,
        "message": "Internal Server Error",
        "description": "The server has encountered a situation it doesn't know how to handle",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "501": {
        "code": 501,
        "message": "Not Implemented",
        "description": "The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "502": {
        "code": 502,
        "message": "Bad Gateway",
        "description": "This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "503": {
        "code": 503,
        "message": "Service Unavailable",
        "description": "The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. Note that together with this response, a user-friendly page explaining the problem should be sent. This responses should be used for temporary conditions and the Retry-After: HTTP header should, if possible, contain the estimated time before the recovery of the service. The webmaster must also take care about the caching-related headers that are sent along with this response, as these temporary condition responses should usually not be cached",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "504": {
        "code": 504,
        "message": "Gateway Timeout",
        "description": "This error response is given when the server is acting as a gateway and cannot get a response in time",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "505": {
        "code": 505,
        "message": "HTTP Version Not Supported",
        "description": "The HTTP version used in the request is not supported by the server",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "506": {
        "code": 506,
        "message": "Variant Also Negotiates",
        "description": "The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "507": {
        "code": 507,
        "message": "Insufficient Storage",
        "description": "The method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value,
        "webdav": True
    },
    "508": {
        "code": 508,
        "message": "Loop Detected",
        "description": "The server detected an infinite loop while processing the request",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value,
        "webdav": True
    },
    "510": {
        "code": 510,
        "message": "Not Extended",
        "description": "Further extensions to the request are required for the server to fulfil it",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
    "511": {
        "code": 511,
        "message": "Network Authentication Required",
        "description": "The 511 status code indicates that the client needs to authenticate to gain network access",
        "category": HTTPStatusCodeCategoryEnum.SERVER_ERROR.value
    },
}

status_codes: dict = {
    **informational,
    **successful,
    **redirection,
    **client_error,
    **server_error
}
