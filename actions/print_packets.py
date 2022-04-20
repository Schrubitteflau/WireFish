from typing import List

from scapy.all import sniff

def print_packets(interfaces: List[str], filter: str = None) -> None:
    # sniff() has count, filter, iface, lfilter, prn, timeout options
    # count : 
    # iface : interface ou liste d'interfaces => "lo" | [ "wlan0", "lo" ]
    #pkts = sniff(count=5,filter="host 64.233.167.99",prn=lambda x:x.summary())
    #help(sniff)
    sniff(iface=interfaces, filter=filter, prn=lambda x:x.summary())
    #print("PACKETS ON IFACE %s and filter %s" % (interface, "<no filter>" if filter is None else filter))
