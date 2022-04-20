#from scapy.all import conf, IFACES, show_interfaces
from scapy.all import get_if_list

# Crash depuis que 2.4.5 -> 2.4.4
def show_interfaces() -> None:
    print(get_if_list())
    #print(conf.ifaces)
    #IFACES.show()
    #show_interfaces()

