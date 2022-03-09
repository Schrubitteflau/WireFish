from typing import Optional, List
import inspect
from termcolor import colored
from scapy.all import *

from sniff_modules.AbstractBaseModule import AbstractBaseModule

ModulesList = List[AbstractBaseModule]

def import_sniff_module(name: str) -> Optional[AbstractBaseModule]:
    to_print = "Loading module %s : " % (colored(name, "yellow"))

    def end_with_error(error: str) -> None:
        print(to_print + colored(error, "red"))
        return None

    try:
        # Dynamically import the module
        imported = __import__("sniff_modules.%s" % (name), fromlist=[ None ])
        ModuleClass = imported.Module
        # It must be a class which extends AbstractBaseModule (so it implements on_receive_packaet(self, packet: Packet))
        if inspect.isclass(ModuleClass):
            module_instance = ModuleClass()
            if isinstance(module_instance, AbstractBaseModule):
                print(to_print + colored("Success", "green"))
                return module_instance
            return end_with_error("Must extends AbstractBaseModule")
        return end_with_error("Must be a class")
    except ModuleNotFoundError:
        return end_with_error("Not found")
    except TypeError as e:
        return end_with_error(str(e))


def load_sniff_modules(modules_names: List[str]) -> ModulesList:
    loaded_modules = []

    for module_name in modules_names:
        module = import_sniff_module(module_name)
        if module is not None:
            loaded_modules.append(module)
    
    return loaded_modules


def process_packet(packet: Packet, modules: ModulesList) -> None:
    for module in modules:
        module.on_receive_packet(packet)


# interface : the name of the interface to listen on ("wlan0", "lo", ...)
# sniff_modules : a comma-separated list of the modules to use ("http.post_credentials,ftp.credentials")
# filter : 
def sniff_data(interface: str, sniff_modules: str, filter: str = None) -> None:

    # [ "http.post_credentials", "ftp.credentials" ]
    modules_names = sniff_modules.split(",")

    print("Sniffing interface %s using filter '%s' and modules %s" % (
        interface,
        "<no filter>" if filter is None else filter,
        modules_names
    ))

    loaded_modules = load_sniff_modules(modules_names)

    sniff(iface=interface, prn=lambda packet: process_packet(packet, loaded_modules))
    #sniff(prn=lambda packet: process_packet(packet, loaded_modules))

