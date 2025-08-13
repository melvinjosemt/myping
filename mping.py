#mping.py
import socket, argparse
from icmp_parser import parse_icmp_reply
from ping_stats import PingStats
from ping_output import print_reply, print_summary

def main():
    parser = argparse.ArgumentParser(description="ENTER AN IPv4")
    parser.add_argument("ip", type=str, help="ipv4")
    parser.add_argument("-c", type=int, help = "Send number of Echo request", default=4)
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    stats = PingStats()
    
    for seq in range(args.c):
        stats.packet_sent()
        result = parse_icmp_reply(sock, args.ip, seq)
        if result["status"] == "success":
            stats.packet_received(result["rtt"])
        print_reply(result)

    print_summary(args.ip, stats.summary())

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("SUDO REQUIRED__PERMISSION NOT ALLOWED")
    except KeyboardInterrupt:
        print("PROGRAM ENDED")     