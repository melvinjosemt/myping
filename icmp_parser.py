from icmp_network import send_icmp_request, receive_reply
from icmp_constants import (ICMP_DEST_UNREACH, ICMP_ECHO_REPLY, 
                            ICMP_HOST_UNREACH, ICMP_NET_UNREACH,
                            ICMP_PORT_UNREACH, ICMP_PROTO_UNREACH )

def parse_icmp_reply(sock, ip, sequence=0):
    identifier, sequence,_, _= send_icmp_request(sock,ip,sequence)
    reply = receive_reply(sock, identifier,sequence)
    
    if reply == None:
        print(f"{ip}:REQUEST TIMED OUT")
        return
    
    rtt = (reply["reply_time"]-reply["start_time"]) * 1000
    
    match (reply["icmp_type"], reply["icmp_code"]):
            case (ICMP_ECHO_REPLY, 0):
                print(f"Reply from {reply['src_ip']}: icmp_seq={reply['sequence']} ident={reply['identifier']} ttl={reply['ttl']} time={rtt:.2f} ms")
            
            case (ICMP_DEST_UNREACH, ICMP_NET_UNREACH):
                print(f"{reply['src_ip']}: Destination Network Unreachable")
            
            case (ICMP_DEST_UNREACH, ICMP_HOST_UNREACH):
                print(f"{reply['src_ip']}: Destination Host Unreachable")
            
            case (ICMP_DEST_UNREACH, ICMP_PROTO_UNREACH):
                print(f"{reply['src_ip']}: Destination Protocol Unreachable")
            
            case (ICMP_DEST_UNREACH, ICMP_PORT_UNREACH):
                print(f"{reply['src_ip']}: Destination Port Unreachable")
            
            case (ICMP_DEST_UNREACH, _):
                print(f"{reply['src_ip']}: Destination Unreachable (code={reply['icmp_code']})")
            
            case _:
                print(f"{reply['src_ip']}: ICMP type={reply['icmp_type']}, code={reply['icmp_code']}")
