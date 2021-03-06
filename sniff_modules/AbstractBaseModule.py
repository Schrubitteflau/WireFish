import os
from typing import Union, Tuple, Any
from abc import ABC, abstractmethod
from datetime import datetime

from termcolor import colored
from scapy.all import Packet

class AbstractBaseModule(ABC):

    _module_name: str = ""

    @abstractmethod
    def on_receive_packet(self, packet: Packet) -> None:
        pass

    def set_module_name(self, name: str) -> None:
        self._module_name = name

    def log(self, message: str, log_type: str = "info", message_color: str = "white") -> None:
        current_time = datetime.now().strftime("%H:%M:%S")
        print("%s - %s - %s : %s" % (
            colored(current_time, "blue"),
            colored(log_type, "white"),
            colored(self._module_name, "yellow"),
            colored(message, message_color)
        ))

    def log_message(self, message: str) -> None:
        self.log(message=message, message_color="white")

    def log_error(self, error_message: str) -> None:
        self.log(message=error_message, log_type="error", message_color="red")

    def write_binary_file(self, filename: str, content: Union[bytes, bytearray], append_flag: bool = False) -> Tuple[str, int]:
        open_mode = "ab" if append_flag else "wb"
        timestamp_now = int(datetime.timestamp(datetime.now()))
        real_filename = "{}_{}".format(timestamp_now, filename)
        file_path = "sniff_files/{}/{}".format(self._module_name, real_filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, open_mode) as file:
                written_size = file.write(content)
                return (file_path, written_size)
        except Exception as e:
            self.log_error(e)

    def to_str_safe(self, data: Any) -> str:
        data_type = type(data)
        if data_type is str:
            return data
        elif data_type is bytes:
            return data.decode("utf-8")
        elif data_type is int or data_type is float:
            return str(data_type)
        elif data is None:
            return "<no-data>"
        return "<AbstractBaseModule.to_str_safe()::unsupported-input>"

