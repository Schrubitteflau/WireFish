from abc import ABC, abstractmethod
from termcolor import colored
from scapy.all import *

class AbstractBaseModule(ABC):

    @property
    @abstractmethod
    def module_name(self) -> str:
        pass

    @abstractmethod
    def on_receive_packet(self, packet: Packet) -> None:
        pass

    def log(self, message: str) -> None:
        current_time = datetime.now().strftime("%H:%M:%S")
        print("%s - %s : %s" % (
            colored(current_time, "blue"),
            colored(self.module_name(), "yellow"),
            message
        ))

