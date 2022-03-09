from scapy.all import *

from sniff_modules.AbstractBaseModule import AbstractBaseModule

class Module(AbstractBaseModule):

    def module_name(self):
        return "ftp.credentials"

    def on_receive_packet(self, packet: Packet) -> None:
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            raw_data = packet[Raw].load

            if raw_data.startswith(b"USER "):
                username = raw_data.split(b"USER ")[1].strip()
                self.log("FTP username : %s " % (username))
            if raw_data.startswith(b"PASSWORD "):
                password = raw_data.split(b"PASSWORD ")[1].strip()
                self.log("FTP password : %s " % (password))

