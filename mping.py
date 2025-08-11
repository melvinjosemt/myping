import socket, argparse
from icmp_parser import parse_icmp_reply

#Constants
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_DEST_UNREACH = 3

def main():
    parser = argparse.ArgumentParser(description="ENTER AN IPv4")
    parser.add_argument("ip", type=str, help="ipv4")
    args = parser.parse_args()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    for seq in range(4):
        parse_icmp_reply(sock, args.ip, seq)

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("SUDO REQUIRED__PERMISSION NOT ALLOWED")
    except KeyboardInterrupt:
        print("PROGRAM ENDED")     