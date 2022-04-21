from scapy.all import Packet, Raw, TCP, IP

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.ftp import FTPPacketParser

class Module(AbstractBaseModule):

    def __init__(self) -> None:
        super().__init__()
        # Command PASV, code 227, reset if code 226
        self.passive_mode = None

    def module_name(self):
        return "ftp.save_files"

    def on_receive_packet(self, packet: Packet) -> None:
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            ftp_packet_parser = FTPPacketParser(packet=packet)

            if ftp_packet_parser.is_entering_passive_mode_response():
                (ip, port) = ftp_packet_parser.get_entering_passive_mode_response_parameters()
                print(ip, port)

