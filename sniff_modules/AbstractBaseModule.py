import os
from typing import Union, Tuple
from abc import ABC, abstractmethod
from datetime import datetime

from termcolor import colored
from scapy.all import Packet

class AbstractBaseModule(ABC):

    @property
    @abstractmethod
    def module_name(self) -> str:
        pass

    @abstractmethod
    def on_receive_packet(self, packet: Packet) -> None:
        pass

    def log(self, message: str, log_type: str = "info", message_color: str = "white") -> None:
        current_time = datetime.now().strftime("%H:%M:%S")
        print("%s - %s - %s : %s" % (
            colored(current_time, "blue"),
            colored(log_type, "white"),
            colored(self.module_name(), "yellow"),
            colored(message, message_color)
        ))

    def log_message(self, message: str) -> None:
        self.log(message=message, message_color="white")

    def log_error(self, error_message: str) -> None:
        self.log(message=error_message, log_type="error", message_color="red")

    def write_file(self, filename: str, content: Union[bytes, bytearray], append_flag: bool = False) -> Tuple[str, int]:
        open_mode = "ab" if append_flag else "wb"
        timestamp_now = int(datetime.timestamp(datetime.now()))
        real_filename = "{}_{}".format(timestamp_now, filename)
        file_path = "sniff_files/{}/{}".format(self.module_name(), real_filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, open_mode) as file:
                written_size = file.write(content)
                return (file_path, written_size)
        except Exception as e:
            self.log_error(e)

