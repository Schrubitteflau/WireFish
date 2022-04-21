import re
from typing import Optional, Tuple

from scapy.all import Packet, Raw
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

    def is_entering_passive_mode_response(self) -> bool:
        return self.is_response_code("227")
    
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
            return (ip, port)
        # Erreur
        return None

