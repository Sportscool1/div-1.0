import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def is_host_up(ip):
    try:
        # Try connecting to port 80 (HTTP) to check if the host is up
        with socket.create_connection((ip, 80), timeout=1):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except socket.error:
        return False

def scan_network(network):
    devices_up = []
    # Create a ThreadPoolExecutor to run the scan concurrently
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for ip in ipaddress.IPv4Network(network):
            futures.append(executor.submit(is_host_up, str(ip)))
        
        for ip, future in zip(ipaddress.IPv4Network(network), futures):
            if future.result():
                devices_up.append(str(ip))
    
    return devices_up

def print_devices(devices):
    print("Online devices found:")
    for device in devices:
        print(device)

if __name__ == "__main__":
    network = "192.168.1.0/24"  # Adjust this to your network's IP range
    devices = scan_network(network)
    print_devices(devices)
