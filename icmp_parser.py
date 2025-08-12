#icmp_parser.py

from icmp_network import send_icmp_request, receive_reply
from icmp_constants import (ICMP_DEST_UNREACH, ICMP_ECHO_REPLY, 
                            ICMP_HOST_UNREACH, ICMP_NET_UNREACH,
                            ICMP_PORT_UNREACH, ICMP_PROTO_UNREACH )

def parse_icmp_reply(sock, ip, sequence=0):
    identifier, sequence,_, _= send_icmp_request(sock,ip,sequence)
    reply = receive_reply(sock, identifier,sequence)
    
    if reply is None:
        return {
            "status" : "timeout",
            "ip" : ip,
            "sequence" : sequence
        }
    
    rtt = (reply["reply_time"] - reply["start_time"]) * 1000
    return {
        "status": "success",
        "ip": reply["src_ip"],
        "sequence": reply["sequence"],
        "identifier": reply["identifier"],
        "ttl": reply["ttl"],
        "icmp_type": reply["icmp_type"],
        "icmp_code": reply["icmp_code"],
        "rtt": rtt
    }