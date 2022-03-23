from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse

from sniff_modules.AbstractBaseModule import AbstractBaseModule

class Module(AbstractBaseModule):

    def module_name(self):
        return "http.post_credentials"

    def on_receive_packet(self, packet: Packet) -> None:

        # haslayer(Raw) is useful for the non-common ports
        # Returns False if a protocol is matched with bind_layers() ?
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            # Ici, packet.haslayer(HTTPRequest) retourne False, donc on fait une inspection manuelle du paquet
            payload_class = self.guess_payload_class(packet[Raw].load)
            if payload_class == HTTPRequest:
                self.handle_http_request(packet=packet, request=HTTPRequest(packet[Raw].load))
            elif payload_class == HTTPResponse:
                self.handle_http_response(packet=packet, response=HTTPResponse(packet[Raw].load))

        if packet.haslayer(HTTPRequest):
            self.handle_http_request(packet=packet, request=packet[HTTPRequest])
        elif packet.haslayer(HTTPResponse):
            self.handle_http_response(packet=packet, response=packet[HTTPResponse])

    # https://github.com/invernizzi/scapy-http/blob/55976e4a5a7b73770f7fd68584c1237ccc15ef46/scapy_http/http.py#L117
    # https://gist.github.com/cr0hn/cfa4e6d04a20f6248a506c072ae0ba81
    def guess_payload_class(self, payload):
        ''' Decides if the payload is an HTTP Request or Response, or something else '''
        try:
            prog = re.compile(
                r"^(?:OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT) "
                r"(?:.+?) "
                r"HTTP/\d\.\d$"
            )
            crlfIndex = payload.index("\r\n".encode())
            req = payload[:crlfIndex].decode("utf-8")
            result = prog.match(req)
            if result:
                return HTTPRequest
            else:
                prog = re.compile(r"^HTTP/\d\.\d \d\d\d .*$")
                result = prog.match(req)
                if result:
                    return HTTPResponse
        except:
            pass
        return None

    def handle_http_request(self, packet: Packet, request: HTTPRequest) -> None:
        request_url = request.Host.decode() + request.Path.decode()
        request_method = request.Method.decode()

        self.log("%s %s" % (request_method, request_url))
        if request_method == "POST" and packet.haslayer(Raw):
            self.log(packet[Raw].load)

    def handle_http_response(self, packet: Packet, response: HTTPResponse) -> None:
        response_code = response.Status_Code
        reponse_set_cookie = response.Set_Cookie

        self.log("Reponse : %s, cookies : %s" % (response_code, reponse_set_cookie))
