from scapy.all import Packet, Raw
from scapy.layers.http import HTTPRequest, HTTPResponse

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.http import HTTPPacketParser

class Module(AbstractBaseModule):

    def on_receive_packet(self, packet: Packet) -> None:
        parser = HTTPPacketParser(packet=packet)
        result_packet = parser.analyze()

        if isinstance(result_packet, HTTPRequest):
            self.handle_http_request(original_packet=packet, request=result_packet)
        elif isinstance(result_packet, HTTPResponse):
            self.handle_http_response(original_packet=packet, response=result_packet)

    def handle_http_request(self, original_packet: Packet, request: HTTPRequest) -> None:
        request_url = self.to_str_safe(request.Host) + self.to_str_safe(request.Path)
        request_method = self.to_str_safe(request.Method)

        self.log_message("%s %s, Authorization header : %s, Cookie header : %s" % (
            request_method,
            request_url,
            self.to_str_safe(request.Authorization),
            self.to_str_safe(request.Cookie)
        ))
        if request_method == "POST" and original_packet.haslayer(Raw):
            self.log_message(original_packet[Raw].load)

    def handle_http_response(self, original_packet: Packet, response: HTTPResponse) -> None:
        self.log_message("Response code : %s, Set-Cookie header : %s" % (
            self.to_str_safe(response.Status_Code),
            self.to_str_safe(response.Set_Cookie)
        ))

