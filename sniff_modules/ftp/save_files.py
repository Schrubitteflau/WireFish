from scapy.all import Packet, Raw, TCP

from sniff_modules.AbstractBaseModule import AbstractBaseModule
from util.packet_analyze.ftp import FTPPacketParser, FTPPassiveModeHandlerCollection

class Module(AbstractBaseModule):

    def __init__(self) -> None:
        super().__init__()
        self._opened_passive_modes = FTPPassiveModeHandlerCollection()

    def module_name(self) -> str:
        return "ftp.save_files"

    def _handle_retr_command(self, filename: str, data: bytearray) -> None:
        written_size = self.write_file(filename=filename, content=data)
        self.log_message("RETR {} : written file of length {} bytes".format(filename, written_size))

    def on_receive_packet(self, packet: Packet) -> None:
        passive_mode_handler = self._opened_passive_modes.get_handler_for_packet(packet=packet)

        if passive_mode_handler is not None:
            passive_mode_handler.handle_packet(packet=packet)

        elif packet.haslayer(TCP) and packet.haslayer(Raw):
            ftp_packet_parser = FTPPacketParser(packet=packet)

            # Code "227" : response for command "PASV"
            if ftp_packet_parser.is_entering_passive_mode_response():
                (ip, port) = ftp_packet_parser.get_entering_passive_mode_response_parameters()
                self._opened_passive_modes.register_handler(client_ip=ip, client_port=port)
                self._opened_passive_modes.print()

            # Code "226", example : "226 Directory send OK." 
            elif ftp_packet_parser.is_transfer_done_response():
                self._opened_passive_modes.destroy_last_created_handler()

            # Code "421 Timeout."
            elif ftp_packet_parser.is_timeout_response():
                self._opened_passive_modes.destroy_all_handlers()
            
            # Retrieve (get/download) a file
            elif ftp_packet_parser.is_command("RETR"):
                filename: str = ftp_packet_parser.get_parameters().decode()
                self.log_message("RETR {}".format(filename))
                # Process :
                # 1 - A PASV command is sent, the server responds with the IP and the PORT the client
                # should connect to in order to send the data
                # 2 - The next command sent by the client specifies the nature of the data which transit
                # between the client and the server : command return ? file content ?
                last_handler = self._opened_passive_modes.get_last_created_handler()
                last_handler.on_stream_end(lambda handler, data : self._handle_retr_command(filename, data))

