import os, time, struct, socket

def checksum(data):
    s = 0
    # Process 2 bytes at a time
    for i in range(0, len(data) - len(data) % 2, 2):
        w = (data[i] << 8) + data[i + 1]
        s += w
    # If odd length, pad last byte
    if len(data) % 2:
        s += data[-1] << 8
    # Add carry bits
    s = (s >> 16) + (s & 0xFFFF)
    s += (s >> 16)
    return ~s & 0xFFFF

def build_icmp_request(identifier, sequence):
    icmp_type = 8  # Echo request
    code = 0
    checksum_icmp = 0
    header = struct.pack('!BBHHH', icmp_type, code, checksum_icmp, identifier, sequence)
    #data = b'hello_icmp'
    send_time = time.time()
    data = struct.pack('!d', send_time) + b'ping_payload'
    checksum_icmp = checksum(header + data)
    header = struct.pack('!BBHHH', icmp_type, code, checksum_icmp, identifier, sequence)
    return header + data


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

def parse_icmp_reply(sock, ip, sequence=0):
    identifier, sequence,_, _= send_icmp_request(sock,ip,sequence)
    reply = receive_reply(sock, identifier,sequence)
    if reply == None:
        print(f"{ip}:REQUEST TIMED OUT")
        return
        
    rtt = (reply["reply_time"]-reply["start_time"]) * 1000
    match (reply["icmp_type"], reply["icmp_code"]):
            case (0, 0):
                print(f"Reply from {reply['src_ip']}: icmp_seq={reply['sequence']} ident={reply['identifier']} ttl={reply['ttl']} time={rtt:.2f} ms")
            case (3, 0):
                print(f"{reply['src_ip']}: Destination Network Unreachable")
            case (3, 1):
                print(f"{reply['src_ip']}: Destination Host Unreachable")
            case (3, 2):
                print(f"{reply['src_ip']}: Destination Protocol Unreachable")
            case (3, 3):
                print(f"{reply['src_ip']}: Destination Port Unreachable")
            case (3, _):
                print(f"{reply['src_ip']}: Destination Unreachable (code={reply['icmp_code']})")
            case _:
                print(f"{reply['src_ip']}: ICMP type={reply['icmp_type']}, code={reply['icmp_code']}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    for seq in range(4):
        parse_icmp_reply(sock,"8.8.8.8", seq)

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("SUDO REQUIRED__PERMISSION NOT ALLOWED")
    except KeyboardInterrupt:
        print("PROGRAM ENDED")     