from typing import Optional, List
import inspect
from termcolor import colored
from scapy.all import *

from sniff_modules.BaseModule import BaseModule

ModulesList = List[BaseModule]

def import_sniff_module(name: str) -> Optional[BaseModule]:
    to_print = "Loading module %s : " % (colored(name, "yellow"))
    try:
        imported = __import__("sniff_modules.%s" % (name), fromlist=[ None ])
        module_class = imported.Module
        if inspect.isclass(module_class):
            module_handler = module_class()
            print(to_print + colored("Success", "green"))
            return module_handler
        print(to_print + colored("Must be a class", "red"))
        return None
    except ModuleNotFoundError:
        print(to_print + colored("Not found", "red"))
        return None
    except TypeError as e:
        print(to_print + colored(e, "red"))
        return None


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
    loaded_modules = load_sniff_modules(modules_names)

    print("Enabling modules %s on interface %s using filter '%s'" % (
        interface,
        modules_names,
        "<no filter>" if filter is None else filter
    ))

    #sniff(iface=interface, prn=lambda packet: process_packet(packet, loaded_modules))

