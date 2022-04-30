from scapy.all import TCP, Packet, Raw

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.ftp import FTPPacketParser

class Module(AbstractBaseModule):

    def module_name(self) -> str:
        return "ftp.credentials"

    def on_receive_packet(self, packet: Packet) -> None:
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            ftp_packet_parser = FTPPacketParser(packet=packet)

            if ftp_packet_parser.is_command("USER"):
                self.log_message("FTP username : %s " % (ftp_packet_parser.get_parameters().decode()))
            elif ftp_packet_parser.is_command("PASS"):
                self.log_message("FTP password : %s " % (ftp_packet_parser.get_parameters().decode()))
