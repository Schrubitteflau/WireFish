from scapy.all import Packet, Raw, NoPayload
from scapy.layers.http import HTTPRequest, HTTPResponse

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.http import HTTPPacketParser
from util.misc import get_random_string

class Module(AbstractBaseModule):

    def __init__(self) -> None:
        super().__init__()
        self._exclude_content_type = [
            "text/css",
            "text/html",
            "application/javascript",
            "font/ttf",
            "font/woff",
            "font/woff2"
        ]

    def on_receive_packet(self, packet: Packet) -> None:
        parser = HTTPPacketParser(packet=packet)
        result_packet = parser.analyze()

        if isinstance(result_packet, HTTPRequest):
            self.handle_http_request(original_packet=packet, request=result_packet)
        elif isinstance(result_packet, HTTPResponse):
            self.handle_http_response(original_packet=packet, response=result_packet)

    def handle_http_request(self, original_packet: Packet, request: HTTPRequest) -> None:
        pass#request.show()

    def handle_http_response(self, original_packet: Packet, response: HTTPResponse) -> None:
        content_type: str = self.to_str_safe(response.Content_Type).split(";")[0]
        if not content_type in self._exclude_content_type and response.haslayer(Raw):
            load = response[Raw].load
            if not isinstance(load, NoPayload):
                (file_path, written_size) = self.write_binary_file(filename=get_random_string(), content=load)
                self.log_message("Written file of type %s as %s (%s bytes)" % (
                    content_type,
                    file_path,
                    written_size
                ))

