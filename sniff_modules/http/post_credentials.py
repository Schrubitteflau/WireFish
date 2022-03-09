from scapy.all import *
from scapy.layers.http import HTTPRequest

from sniff_modules.AbstractBaseModule import AbstractBaseModule

class Module(AbstractBaseModule):
    def on_receive_packet(self, packet: Packet) -> None:
        if packet.haslayer(HTTPRequest):
            request = packet[HTTPRequest]

            request_url = request.Host.decode() + request.Path.decode()
            request_method = request.Method.decode()

            print("%s %s" % (request_method, request_url))
            if request_method == "POST" and packet.haslayer(Raw):
                print(packet[Raw].load)

