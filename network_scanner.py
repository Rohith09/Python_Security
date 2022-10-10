import optparse

import scapy.all as scapy


def get_ip():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip_address", dest="ip", help="Please enter your IP address") 
    (options, arguments) = parser.parse_args() # options can be anything, it is just a variable name 
    if not options.ip: # (dest has to be used here from add option)
        parser.error("---------------- Please specify IP address---------------------")
    return options #(this is really important or else we get None returned)


def scan(ip_address):
    arp_request = scapy.ARP(pdst=ip_address) # creates an blank ARP data frame 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # creates a blank Ethernet frame (all possible MAC addresses)
    broadcast_arp_request = broadcast / arp_request #this is the encapsulation function which combines both the ARP data frame and the Ethernet frame. The sequence is important Broadcast and then the Ethernet frame 
    (answered, unanswered) = scapy.srp(broadcast_arp_request, timeout=1) # to send the data pack to LAN
    # print(answered.summary())
    print("--------------------------------------")
    print("IP address" + "\t\t" + "MAC Address")
    print("---------------------------------------")
    for element in answered:
        print(element[1].psrc, "\t\t", element[1].hwdst)
        print("-----------------------------------")
    # print(element[1].show())


ip_user_input = get_ip()

scan(ip_user_input.ip)
