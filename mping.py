#mping.py
import socket, argparse, time
from icmp_parser import parse_icmp_reply
from ping_stats import PingStats
from ping_output import print_reply, print_summary

def arguments():
    parser = argparse.ArgumentParser(description="ENTER AN IPv4")
    parser.add_argument("ip", type=str, help="ipv4")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--count", type=int, help = "Send number of Echo request")
    group.add_argument("-t", action="store_true", help = "Continious ping until exixted")
    args = parser.parse_args()
    if not args.count and not args.t:
        args.count = 4
    return args

def run_ping(args, stats, sock):
    seq = 0
    try:
        if args.t:
            while True:
                stats.packet_sent()
                result = parse_icmp_reply(sock, args.ip, seq)
                seq += 1
                if result["status"] == "success":
                    stats.packet_received(result["rtt"])
                print_reply(result)
                time.sleep(1)

        elif args.count:  # default 4 if not provided
            for seq in range(args.count):
                stats.packet_sent()
                result = parse_icmp_reply(sock, args.ip, seq)
                if result["status"] == "success":
                    stats.packet_received(result["rtt"])
                print_reply(result)
                time.sleep(1)
            print_summary(args.ip, stats.summary())    

    except KeyboardInterrupt:
        print_summary(args.ip, stats.summary())



def main():
    args = arguments()
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    stats = PingStats()
    run_ping(args, stats, sock)

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("Sudo required") 