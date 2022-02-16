from scapy.layers.http import *

def on_receive_packet(packet: Packet) -> None:
    packet.summary()
    pass

