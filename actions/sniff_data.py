from typing import Optional, List
import inspect

from termcolor import colored
from scapy.all import Packet, sniff
from sniff_modules.AbstractBaseModule import AbstractBaseModule

ModulesList = List[AbstractBaseModule]

def import_sniff_module(name: str) -> Optional[AbstractBaseModule]:
    to_print = "Loading module %s : " % (colored(name, "yellow"))

    def end_with_error(error: str) -> None:
        print(to_print + colored(error, "red"))

    try:
        # Dynamically import the module
        imported = __import__("sniff_modules.%s" % (name), fromlist=[ None ])
        ModuleClass = imported.Module
        # It must be a class which extends AbstractBaseModule
        if inspect.isclass(ModuleClass):
            module_instance = ModuleClass()
            if isinstance(module_instance, AbstractBaseModule):
                module_instance.set_module_name(name)
                print(to_print + colored("Success", "green"))
                return module_instance
            end_with_error("Must extends AbstractBaseModule")
            return None
        end_with_error("Must be a class")
        return None
    except ModuleNotFoundError as e:
        # This error is also raised if the module code contains an error
        end_with_error("Not found or error : %s" % (e))
        return None
    except TypeError as e:
        end_with_error(str(e))
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


# interface : the interface(s) to listen on ("wlan0", "lo", ...)
# sniff_modules : a comma-separated list of the modules to use ("http.post_credentials,ftp.credentials")
# filter : 
def sniff_data(interfaces: List[str], sniff_modules: List[str], filter: str = None) -> None:

    print("Sniffing interface %s using filter '%s' and modules %s" % (
        interfaces,
        "<no filter>" if filter is None else filter,
        sniff_modules
    ))

    loaded_modules = load_sniff_modules(sniff_modules)

    sniff(iface=interfaces, prn=lambda packet: process_packet(packet, loaded_modules))

