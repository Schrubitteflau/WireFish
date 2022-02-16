import typing

from scapy.all import *

SniffModuleHandler = typing.Callable[ [ Packet ], None ]

def import_sniff_module(name: str) -> typing.Optional[SniffModuleHandler]:
    try:
        imported = __import__("sniff_modules.%s" % (name), fromlist=[ None ])
        module_handler = imported.on_receive_packet
        return module_handler
    except ModuleNotFoundError:
        return None


def load_sniff_modules(modules_names: typing.List[str]) -> List[SniffModuleHandler]:
    loaded_modules = []

    for module_name in modules_names:
        module = import_sniff_module(module_name)
        if module is None:
            print("Module '%s' not found" % (module_name))
        else:
            loaded_modules.append(module)
    
    return loaded_modules


# interface : the name of the interface to listen on ("wlan0", "lo", ...)
# sniff_modules : a comma-separated list of the modules to use ("http.post_credentials,ftp.credentials")
# filter : 
def sniff_data(interface: str, sniff_modules: str, filter: str = None) -> None:

    # [ "http.post_credentials", "ftp.credentials" ]
    modules_names = sniff_modules.split(",")
    loaded_modules = load_sniff_modules(modules_names)

    print(loaded_modules)

    print("Enabling modules %s on interface %s using filter '%s'" % (
        interface,
        modules_names,
        "<no filter>" if filter is None else filter
    ))

