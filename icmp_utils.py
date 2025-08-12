#icmp_utils.py

import struct, time
from icmp_constants import ICMP_ECHO_REQUEST

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
    icmp_type = ICMP_ECHO_REQUEST  # Echo request
    code = 0
    checksum_icmp = 0
    header = struct.pack('!BBHHH', icmp_type, code, checksum_icmp, identifier, sequence)
    #data = b'hello_icmp'
    send_time = time.time()
    data = struct.pack('!d', send_time) + b'ping_payload'
    checksum_icmp = checksum(header + data)
    header = struct.pack('!BBHHH', icmp_type, code, checksum_icmp, identifier, sequence)
    return header + data