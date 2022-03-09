from scapy.all import *
from scapy.layers.http import HTTPRequest

from sniff_modules.AbstractBaseModule import AbstractBaseModule

class Module(AbstractBaseModule):

    def module_name(self):
        return "http.post_credentials"

    def on_receive_packet(self, packet: Packet) -> None:
        if packet.haslayer(HTTPRequest):
            request = packet[HTTPRequest]

            request_url = request.Host.decode() + request.Path.decode()
            request_method = request.Method.decode()

            self.log("%s %s" % (request_method, request_url))
            if request_method == "POST" and packet.haslayer(Raw):
                self.log(packet[Raw].load)

