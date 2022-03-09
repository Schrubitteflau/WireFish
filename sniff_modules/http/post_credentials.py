from scapy.layers.http import *
from sniff_modules.BaseModule import BaseModule

class Module(BaseModule):
    def on_receive_packet(self, packet: Packet) -> None:
        packet.summary()
        pass

