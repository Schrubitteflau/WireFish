import re
from typing import Optional, Tuple, Dict, Callable, Any

from scapy.all import Packet, Raw, IP, TCP, NoPayload
from util.misc import add_space_and_encode_to_bytes

passive_mode_response_regex = re.compile(
    r"Entering Passive Mode \((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)"
)

class FTPPacketParser:
    def __init__(self, packet: Packet) -> None:
        self._packet = packet
        self._raw_data: str = packet[Raw].load
        self._matched_command: Optional[str] = None
        self._parameters: Optional[bytes] = None

    def is_command(self, command_name: str) -> Optional[str]:
        if self._matched_command is not None:
            return self._matched_command

        result = self._raw_data.startswith(add_space_and_encode_to_bytes(command_name))
        if result:
            # We store the last matched command, because a packet can't be related to several commands at once
            self._matched_command = command_name
        return result

    def get_parameters(self) -> bytes:
        if self._matched_command is not None:
            if self._parameters is None:
                self._parameters = self._raw_data.split(add_space_and_encode_to_bytes(self._matched_command))[1].strip()
            return self._parameters
        return b""

    def is_response_code(self, response_code: str) -> bool:
        # We handle a response code as a command : a string which prefix the rest of the data separated by a space
        return self.is_command(response_code)

    # See more about passive mode : https://www.deskshare.com/resources/articles/ftp-how-to.aspx
    def is_entering_passive_mode_response(self) -> bool:
        return self.is_response_code("227")

    # https://fr.wikipedia.org/wiki/Liste_des_codes_des_r%C3%A9ponses_d%27un_serveur_FTP
    def is_transfer_done_response(self) -> bool:
        return self.is_response_code("226")
    
    def is_timeout_response(self) -> bool:
        return self.is_response_code("421")

    def get_entering_passive_mode_response_parameters(self) -> Tuple[str, int]:
        """
            You must ensure that is_entering_passive_mode_response() returns true before calling this method
            The first element of the return tuple is the IP address, and the second is the port
        """
        params = self.get_parameters().decode()
        print(params)
        result = passive_mode_response_regex.search(params)
        if result is not None:
            ip = "{}.{}.{}.{}".format(
                result.group(1),
                result.group(2),
                result.group(3),
                result.group(4)
            )
            port_octet_1 = int(result.group(5))
            port_octet_2 = int(result.group(6))
            port = port_octet_1 * 256 + port_octet_2
            # It means that the server expects the client to send the data in the specified IP and PORT
            return (ip, port)
        # Erreur
        return None



class FTPPassiveModeHandler:
    def __init__(self, client_ip: str, client_port: int) -> None:
        self._client_ip: str = client_ip
        self._client_port: int = client_port
        self._data: bytearray = bytearray()
        # Callback called when the instance is destroyed
        # This FTPPassiveModeHandler instance should be destroyed by a FTPPassiveModeHandlerCollection
        # when there's no data anymore
        self._on_stream_end_callback: Optional[Callable[[FTPPassiveModeHandler, bytearray], None]] = None

    def __del__(self) -> None:
        if callable(self._on_stream_end_callback):
            self._on_stream_end_callback(self, self._data)

    # Signature of callback should be : Callable[[FTPPassiveModeHandler, bytearray], None]
    def on_stream_end(self, callback: Callable[[Any, bytearray], None]):
        self._on_stream_end_callback = callback

    def handle_packet(self, packet: Packet) -> None:
        # We assume that the packet has already been checked before and that it is destinated to this handler
        payload = packet[TCP].payload
        if not isinstance(payload, NoPayload):
            raw_data: bytes = payload.load
            self._data.extend(raw_data)
            print("{}:{} => handle payload size : {}".format(self._client_ip, self._client_port, len(payload)))


class FTPPassiveModeHandlerCollection:
    def __init__(self) -> None:
        # Key : "IP:PORT", value : FTPPassiveModeHandler instance
        self._passive_mode_handlers: Dict = {}
        self._last_created_handler_key: Optional[str] = None

    def _make_key(self, ip: str, port: int) -> str:
        return "{}:{}".format(ip, port)

    def _retrieve_handler(self, client_ip: str, client_port: int) -> Optional[FTPPassiveModeHandler]:
        key = self._make_key(ip=client_ip, port=client_port)
        if key in self._passive_mode_handlers:
            return self._passive_mode_handlers[key]
        return None

    def register_handler(self, client_ip: str, client_port: int) -> None:
        key = self._make_key(ip=client_ip, port=client_port)
        handler = FTPPassiveModeHandler(client_ip=client_ip, client_port=client_port)
        self._passive_mode_handlers[key] = handler
        self._last_created_handler_key = key

    def destroy_last_created_handler(self) -> None:
        if self._last_created_handler_key is not None:
            del self._passive_mode_handlers[self._last_created_handler_key]
            self._last_created_handler_key = None

    def destroy_all_handlers(self) -> None:
        self._passive_mode_handlers.clear()
    
    def get_last_created_handler(self) -> Optional[FTPPassiveModeHandler]:
        if self._last_created_handler_key is not None:
            return self._passive_mode_handlers[self._last_created_handler_key]
        return None
    
    def print(self) -> None:
        print(self._passive_mode_handlers)

    def get_handler_for_packet(self, packet: Packet) -> Optional[FTPPassiveModeHandler]:
        if len(self._passive_mode_handlers) > 0 and packet.haslayer(IP) and packet.haslayer(TCP):
            # Based on source IP and PORT
            ip_src=packet[IP].src
            tcp_sport=packet[TCP].sport
            handler = self._retrieve_handler(client_ip=ip_src, client_port=tcp_sport)

            # Based on destination IP and PORT
            if handler is None:
                ip_dst=packet[IP].dst
                tcp_dport=packet[TCP].dport
                handler = self._retrieve_handler(client_ip=ip_dst, client_port=tcp_dport)
            
            return handler

