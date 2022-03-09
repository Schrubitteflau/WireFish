from scapy.all import *
from scapy.layers.http import HTTPRequest
from sniff_modules.AbstractBaseModule import AbstractBaseModule

class Module(AbstractBaseModule):
    def on_receive_packaet(self, packet: Packet) -> None:
        if packet.haslayer(HTTPRequest):
            # if this packet is an HTTP Request
            # get the requested URL
            url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
            # get the requester's IP Address
            ip = packet[IP].src
            # get the request method
            method = packet[HTTPRequest].Method.decode()
            print(f"\n[+] {ip} Requested {url} with {method}")
            if show_raw and packet.haslayer(Raw) and method == "POST":
                # if show_raw flag is enabled, has raw data, and the requested method is "POST"
                # then show raw
                print(f"\n[*] Some useful Raw data: {packet[Raw].load}")

