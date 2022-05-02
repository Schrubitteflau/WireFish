import os
from typing import Union, Tuple, Any
from abc import ABC, abstractmethod
from datetime import datetime

from termcolor import colored
from scapy.all import Packet

from scapy.all import Packet, Raw
from scapy.layers.http import HTTPRequest, HTTPResponse

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.http import HTTPPacketParser

class AbstractHTTPModule(AbstractBaseModule):

    def on_receive_packet(self, packet: Packet) -> None:
        parser = HTTPPacketParser(packet=packet)
        result_packet = parser.analyze()

        if isinstance(result_packet, HTTPRequest):
            self.handle_http_request(original_packet=packet, request=result_packet)
        elif isinstance(result_packet, HTTPResponse):
            self.handle_http_response(original_packet=packet, response=result_packet)

    @abstractmethod
    def handle_http_request(self, original_packet: Packet, request: HTTPRequest) -> None:
        pass

    @abstractmethod
    def handle_http_response(self, original_packet: Packet, response: HTTPResponse) -> None:
        pass

