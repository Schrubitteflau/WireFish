from abc import ABC, abstractmethod
from scapy.all import *

class BaseModule(ABC):
    @abstractmethod
    def on_receive_packet(self, packet: Packet) -> None:
        pass

