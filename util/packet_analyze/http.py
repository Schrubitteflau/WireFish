import re
from enum import Enum
from typing import Optional, Union

from scapy.all import Packet, TCP, Raw
from scapy.layers.http import HTTPRequest, HTTPResponse

http_request_regex = re.compile(
    r"^(?:OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT) "
    r"(?:.+?) "
    r"HTTP/\d\.\d$"
)
http_response_regex = re.compile(r"^HTTP/\d\.\d \d\d\d .*$")

class PayloadClass(Enum):
    HTTP_REQUEST = 1
    HTTP_RESPONSE = 2
    UNKNOWN = 3

class HTTPPacketParser:
    def __init__(self, packet: Packet) -> None:
        self._packet = packet

    # https://github.com/invernizzi/scapy-http/blob/55976e4a5a7b73770f7fd68584c1237ccc15ef46/scapy_http/http.py#L117
    # https://gist.github.com/cr0hn/cfa4e6d04a20f6248a506c072ae0ba81
    def _guess_payload_class(self, payload) -> PayloadClass:
        """ Decides if the payload is an HTTP Request or Response, or something else """
        try:
            crlfIndex = payload.index("\r\n".encode())
            req = payload[:crlfIndex].decode("utf-8")
            if http_request_regex.match(req):
                return PayloadClass.HTTP_REQUEST
            elif http_response_regex.match(req):
                return PayloadClass.HTTP_RESPONSE
        except:
            pass
        return PayloadClass.UNKNOWN

    def analyze(self) -> Optional[Union[HTTPRequest, HTTPResponse]]:
        packet = self._packet

        # Si port == 80 et que les données correspondent bien à une requête/réponse HTTP
        if packet.haslayer(HTTPRequest):
            return packet[HTTPRequest]
            #self.handle_http_request(packet=packet, request=packet[HTTPRequest])
        elif packet.haslayer(HTTPResponse):
            return packet[HTTPResponse]
            #self.handle_http_response(packet=packet, response=packet[HTTPResponse])

        # haslayer(Raw) est utile pour accéder aux données de ports non-communs (ou non gérés par scapy)
        # Returns False if a protocol is matched with bind_layers() ?
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            # Inspection manuelle du payload du paquet
            payload_class = self._guess_payload_class(packet[Raw].load)
            if payload_class == PayloadClass.HTTP_REQUEST:
                return HTTPRequest(packet[Raw].load)
                #self.handle_http_request(packet=packet, request=HTTPRequest(packet[Raw].load))
            elif payload_class == PayloadClass.HTTP_RESPONSE:
                return HTTPResponse(packet[Raw].load)
                #self.handle_http_response(packet=packet, response=HTTPResponse(packet[Raw].load))

