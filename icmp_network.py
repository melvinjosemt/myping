#icmp_network.py

from icmp_utils import build_icmp_request
import struct, socket, time, os


def send_icmp_request(sock, ip, sequence=0):
    identifier = os.getpid() & 0xFFFF
    #sequence = 0
    icmp_packet = build_icmp_request(identifier, sequence)
    timestamp = struct.unpack('!d', icmp_packet[8:16]) [0]
    
    try:
        sock.sendto(icmp_packet, (ip,0))
    except OSError as e:
        print(f"ERROR OCCURED:{e}")
    except Exception as e:
        print(f"EXCEPTION:{e}")

    return identifier, sequence , timestamp, ip     

def receive_reply(sock, request_identifier, request_sequence, timeout=1):
    sock.settimeout(timeout)

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            reply_time = time.time()
        except socket.timeout:
            #print("REQUEST TIMED OUT")
            return None

        ihl = data[0] & 0x0F
        ip_header_length = ihl * 4
        ip_header = data[:ip_header_length]
        icmp_header= data[ip_header_length:ip_header_length+8]
        payload = data[ip_header_length+8:]
        src_ip = socket.inet_ntoa(ip_header[12:16])
        ttl = ip_header[8]
        icmp_type = icmp_header[0]
        icmp_code = icmp_header[1]
        start_time = struct.unpack('!d', payload[:8])[0]
        icmp_sequence = struct.unpack('!H', icmp_header[6:8])[0]
        icmp_identifier = struct.unpack('!H', icmp_header[4:6])[0]

        if icmp_identifier != request_identifier or icmp_sequence != request_sequence:
            continue

        return {
            "src_ip": src_ip,
            "ttl": ttl,
            "icmp_type": icmp_type,
            "icmp_code": icmp_code,
            "identifier": icmp_identifier,
            "sequence": icmp_sequence,
            "start_time": start_time,
            "reply_time": reply_time
        }