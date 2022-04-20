import re
from typing import Optional, Union

from scapy.layers.http import HTTPRequest, HTTPResponse

http_request_regex = re.compile(
    r"^(?:OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT) "
    r"(?:.+?) "
    r"HTTP/\d\.\d$"
)
http_response_regex = re.compile(r"^HTTP/\d\.\d \d\d\d .*$")

# https://github.com/invernizzi/scapy-http/blob/55976e4a5a7b73770f7fd68584c1237ccc15ef46/scapy_http/http.py#L117
# https://gist.github.com/cr0hn/cfa4e6d04a20f6248a506c072ae0ba81
def guess_payload_class(payload) -> Optional[Union[HTTPRequest, HTTPResponse]]:
    ''' Decides if the payload is an HTTP Request or Response, or something else '''
    try:
        crlfIndex = payload.index("\r\n".encode())
        req = payload[:crlfIndex].decode("utf-8")
        if http_request_regex.match(req):
            return HTTPRequest
        elif http_response_regex.match(req):
            return HTTPResponse
    except:
        pass
    return None

