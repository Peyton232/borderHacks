from scapy.all import *


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
ip_address = input("Enter a valid IP")

scan(ip_address)






