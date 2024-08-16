from scapy.all import ARP, Ether, srp
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/scan')
def scan():
    ip_range = "192.168.1.0/24"  # Adjust this to your network's IP range
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return jsonify(devices)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
