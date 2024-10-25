import time
import threading
import queue
import pydivert
from scapy.all import IP, UDP

# Queue to hold packets for processing
packet_queue = queue.Queue()

# Array to store destination IPs
dest_ips = []

# Flag to signal threads to stop
stop_event = threading.Event()

def packet_handler(w, chosen_country, chosen_region, get_geo_data):
    while not stop_event.is_set():
        try:
            packet, timestamp, dest_ip = packet_queue.get(timeout=1)
            try:
                # Fetch geolocation data for the destination IP
                geo_data = get_geo_data(dest_ip)

                if 'error' in geo_data:
                    print(f"Error fetching data for IP {dest_ip}: {geo_data['error']}")
                    continue

                country = geo_data['country']
                region = geo_data['region']

                print(f"Fetched data about IP {dest_ip}: Country={country}, Region={region}")

                # Check if the fetched geo data matches the user specified geo data
                if country == chosen_country and region == chosen_region:
                    # Re-inject the packet back into the network stack
                    w.send(packet)
                    print(f"Packet forwarded for IP {dest_ip}")
                else:
                    print(f"Packet discarded for IP {dest_ip}: Does not match user-specified data (Country={chosen_country}, Region={chosen_region})")
            except OSError as e:
                print(f"Error re-injecting packet: {e}")
            packet_queue.task_done()
        except queue.Empty:
            continue

def capture_packets(chosen_country, chosen_region, get_geo_data):
    # Open a WinDivert handle to capture outbound packets
    with pydivert.WinDivert("outbound and udp") as w:
        # Start the packet handler thread
        handler_thread = threading.Thread(target=packet_handler, args=(w, chosen_country, chosen_region, get_geo_data), daemon=True)
        handler_thread.start()

        print("Waiting for packets...")
        try:
            for packet in w:
                if stop_event.is_set():
                    print(f"Destination IPs ({len(dest_ips)}): {dest_ips}")
                    break
                try:
                    raw_packet = bytes(packet.raw)
                    scapy_packet = IP(raw_packet)
                    
                    if (UDP in scapy_packet and
                        len(scapy_packet) == 159 and
                        len(scapy_packet[UDP].payload) == 131 and
                        scapy_packet.proto == 17 and
                        scapy_packet[UDP].dport not in [80, 443]):
                        
                        print(f"Captured matching UDP packet: {scapy_packet.summary()}")
                        
                        packet_queue.put((packet, time.time(), scapy_packet.dst))
                    else:
                        w.send(packet)
                except Exception as e:
                    print(f"Error processing packet: {e}")
        except KeyboardInterrupt:
            print("Stopping...")
            stop_event.set()
            handler_thread.join()