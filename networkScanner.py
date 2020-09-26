from scapy.all import *
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP Address/Adresses')
    options = parser.parse_args()

    # Check for errors i.e if the user does not specify the target IP Address
    # Quit the program if the argument is missing
    # While quitting also display an error message
    if not options.target:
        # Code to handle if interface is not specified
        parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options

def scan(ip):

    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = srp(arp_request_broadcast,timeout=1,verbose = True)[0]
    print("IP\t\t\tMAC Address\n-------------------------------")
    clients_list = []
    if not answered:
        print("No clients responded\n")
    else:
        for element in answered:
            client_dict = {"ip": element[1].psrc,"mac": element[1].hwsrc}
            clients_list.append(client_dict)
            print(element[1].psrc + "\t\t" + element[1].hwsrc)
       # print(clients_list)



options = get_args()
scan_result = scan(options.target)



