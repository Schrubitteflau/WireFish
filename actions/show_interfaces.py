from tabulate import tabulate

import netifaces

# Depuis le downgrade de 2.4.5 vers 2.4.4, impossible d'importer les éléments suivants
# depuis scapy.all (ils ne sont disponibles que pour Windows, voir scapy/arch/windows/__init__.py)
# - IFACES, pour IFACES.show()
# - conf.ifaces n'est pas défini, seul conf.iface l'est
# - show_interfaces(), qui utilise IFACES.show()
# Donc fonction recodée à la main en utilisant un autre module : netifaces, qui est cross-platform
def show_interfaces() -> None:
    interfaces = netifaces.interfaces()
    interfaces_details = []

    for interface in interfaces:
        name = interface
        if_addresses = netifaces.ifaddresses(name)
        mac = if_addresses.get(netifaces.AF_LINK)
        ipv4 = if_addresses.get(netifaces.AF_INET)
        ipv6 = if_addresses.get(netifaces.AF_INET6)

        mac_address = "" if mac is None else mac[0].get("addr")
        ipv4_address = "" if ipv4 is None else ipv4[0].get("addr")
        ipv6_address = "" if ipv6 is None else ipv6[0].get("addr").split("%")[0]

        interface_details = [ name, mac_address, ipv4_address, ipv6_address ]
        interfaces_details.append(interface_details)

    print(tabulate(tabular_data=interfaces_details, headers=["Name", "MAC", "IPv4", "IPv6"]))

