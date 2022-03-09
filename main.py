#! wirefish-venv/bin/python

import argparse
from scapy.all import *

from actions import *
import actions

interfaces = get_if_list()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    help="Actions help",
    dest="command_action",
    required=True
)

# Parser for the show-interfaces action
parser_show_interfaces = subparsers.add_parser(
    "show-interfaces",
    help="shows all available interfaces and their details"
)

# Parser for the print-packets action
parser_print_packets = subparsers.add_parser(
    "print-packets",
    help="starts listening to the packet through the specified interface"
)

# Argument used to specify the interface to listen packets on
parser_print_packets.add_argument(
    "-I",
    "--interface",
    dest="interface",
    action="store",
    choices=interfaces,
    required=True
)

# This optional argument allows us to specify a filter to apply before printing the packets
parser_print_packets.add_argument(
    "-F",
    "--filter",
    dest="filter",
    action="store",
    required=False
)

# Parser for the sniff-data action
parser_sniff_data = subparsers.add_parser(
    "sniff-data",
    help="starts listening to the packet through the specified interface"
)

args = parser.parse_args()
command_action = args.command_action

try:
    if command_action == "show-interfaces":
        actions.show_interfaces()
    elif command_action == "print-packets":
        actions.print_packets(
            interface=args.interface,
            filter=args.filter
        )
    elif command_action == "sniff-data":
        actions.sniff_data(
            #interface="lo",
            interface="wlp164s0",
            sniff_modules="ftp.credentials"
            #sniff_modules="http.post_credentials,ftp.credentials"
            #interface=args.interface,
            #modules=args.modules,
            #filter=args.filter
        )
except PermissionError:
    print("You need to be root !")

print(args)
