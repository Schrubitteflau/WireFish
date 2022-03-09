from abc import ABC, abstractmethod
from scapy.all import *

class AbstractBaseModule(ABC):
    @abstractmethod
    def on_receive_packet(self, packet: Packet) -> None:
        pass

