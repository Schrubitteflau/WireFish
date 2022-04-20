import re
from typing import Optional, Tuple

from scapy.all import Packet, Raw
from util.misc import add_space_and_encode_to_bytes

class FTPPacketParser:
    def __init__(self, packet: Packet) -> None:
        self._packet = packet
        self._raw_data: str = packet[Raw].load
        self._passive_mode_response_regex = re.compile(
            r"Entering Passive Mode \((\d),(\d),(\d),(\d),(\d),(\d)\)"
        )
        self._matched_command = None

    def is_command(self, command_name: str) -> Optional[str]:
        if self._matched_command is not None:
            return self._matched_command

        result = self._raw_data.startswith(add_space_and_encode_to_bytes(command_name))
        if result:
            # We store the last matched command, because a packet can't be related to several commands at once
            self._matched_command = command_name
        return result

    def get_parameters(self) -> str:
        if self._matched_command is not None:
            return self._raw_data.split(add_space_and_encode_to_bytes(self._matched_command))[1].strip()
        return ""

    def is_response_code(self, response_code: str) -> bool:
        # We handle a response code as a command : a string which prefix the rest of the data separated by a space
        return self.is_command(response_code)

    def is_entering_passive_mode_response(self) -> Tuple[str, int]:
        """ The first element of the return tuple is the IP address, and the second is the port """
        if (self.is_response_code("227")):
            params = self.get_parameters("227")
            # Example value : Entering Passive Mode (192,168,30,95,171,34)
            result = re.search(self._passive_mode_response_regex, params)
            print(result.groups())

        return None
