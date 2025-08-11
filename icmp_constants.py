# icmp_constants.py
"""
ICMP type and code constants.
Source: RFC 792 + common ICMP extensions.
"""

# ICMP Types
ICMP_ECHO_REPLY = 0
ICMP_DEST_UNREACH = 3
ICMP_ECHO_REQUEST = 8

# Destination Unreachable Codes(3)
ICMP_NET_UNREACH = 0
ICMP_HOST_UNREACH = 1
ICMP_PROTO_UNREACH = 2
ICMP_PORT_UNREACH = 3
