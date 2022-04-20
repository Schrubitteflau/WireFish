#! wirefish-venv/bin/python

import argparse
from scapy.all import *

import actions

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    help="Shows the help of the actions",
    dest="command_action",
    required=True
)

# Parser for the show-interfaces action
parser_show_interfaces = subparsers.add_parser(
    "show-interfaces",
    help="Shows all available interfaces and their details"
)

# Parser for the print-packets action
parser_print_packets = subparsers.add_parser(
    "print-packets",
    help="Starts listening the specified interface(s) and prints the summary of the intercepted packets"
)

# Argument used to specify the interface to listen packets on
parser_print_packets.add_argument(
    "-I",
    "--interface",
    dest="interface",
    action="store",
    required=True,
    help="A comma-separated list of the interface(s) to listen on, or the value 'ALL'. For example : 'wlan0,lo,eth1'"
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
    help="Starts listening the specified interface(s) and analyze the packets with the specified modules"
)

parser_sniff_data.add_argument(
    "-I",
    "--interfaces",
    dest="interfaces",
    action="store",
    required=True,
    help="A comma-separated list of the interface(s) to listen on, or the value 'ALL'. For example : 'wlan0,lo,eth1'"
)

parser_sniff_data.add_argument(
    "-M",
    "--modules",
    dest="modules",
    action="store",
    required=True,
    help="A comma-separated list of the modules to use. For example : 'http.post_credentials,ftp.credentials'"
)

args = parser.parse_args()
command_action = args.command_action

try:
    if command_action == "show-interfaces":
        actions.show_interfaces()
    elif command_action == "print-packets":
        interfaces = get_if_list() if args.interfaces == "ALL" else args.interfaces.split(",")
        actions.print_packets(
            interfaces=interfaces,
            filter=args.filter
        )
    elif command_action == "sniff-data":
        sniff_modules = args.modules.split(",")
        interfaces = get_if_list() if args.interfaces == "ALL" else args.interfaces.split(",")
        actions.sniff_data(
            sniff_modules=["http.post_credentials","ftp.credentials"],
            #sniff_modules=sniff_modules,
            interfaces=interfaces,
            #filter=args.filter
        )

except PermissionError:
    print("You need to be root !")

print(args)
