#ping_output.py

def print_reply(result):
    if result["status"] == "timeout":
        print(f"{result['ip']}: REQUEST TIMED OUT")
    else:
        print(f"Reply from {result['ip']}: icmp_seq={result['sequence']} ident={result['identifier']} ttl={result['ttl']} time={result['rtt']:.2f} ms")

def print_summary(ip, summary):
    print(f"\n--- {ip} ping statistics ---")
    print(f"{summary['sent']} packets transmitted, {summary['received']} received, {summary['loss']:.0f}% packet loss")
    if summary["min"] is not None:
        print(f"rtt min/avg/max = {summary['min']:.2f}/{summary['avg']:.2f}/{summary['max']:.2f} ms")

