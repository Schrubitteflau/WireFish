from typing import Optional, Union
from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.http import guess_payload_class

class Module(AbstractBaseModule):

    def module_name(self) -> str:
        return "http.post_credentials"

    def on_receive_packet(self, packet: Packet) -> None:

        # haslayer(Raw) est utile pour accéder aux données de ports non-communs (ou non gérés par scapy)
        # Returns False if a protocol is matched with bind_layers() ?
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            # Ici, packet.haslayer(HTTPRequest) retourne False, donc on fait une inspection manuelle du paquet
            payload_class = guess_payload_class(packet[Raw].load)
            if payload_class == HTTPRequest:
                self.handle_http_request(packet=packet, request=HTTPRequest(packet[Raw].load))
            elif payload_class == HTTPResponse:
                self.handle_http_response(packet=packet, response=HTTPResponse(packet[Raw].load))

        # Si port == 80 et que les données correspondent bien à une requête/réponse HTTP
        if packet.haslayer(HTTPRequest):
            self.handle_http_request(packet=packet, request=packet[HTTPRequest])
        elif packet.haslayer(HTTPResponse):
            self.handle_http_response(packet=packet, response=packet[HTTPResponse])

    def handle_http_request(self, packet: Packet, request: HTTPRequest) -> None:
        request_url = request.Host.decode() + request.Path.decode()
        request_method = request.Method.decode()

        self.log_message("%s %s" % (request_method, request_url))
        if request_method == "POST" and packet.haslayer(Raw):
            self.log_message(packet[Raw].load)

    def handle_http_response(self, packet: Packet, response: HTTPResponse) -> None:
        response_code = response.Status_Code
        reponse_set_cookie = response.Set_Cookie

        self.log_message("Reponse : %s, cookies : %s" % (response_code, reponse_set_cookie))
