#ping_stats.py

class PingStats:
    def __init__(self):
        self.sent = 0
        self.received = 0
        self.rtts = []

    def packet_sent(self):
        self.sent += 1

    def packet_received(self, rtt):
        self.received += 1
        self.rtts.append(rtt)

    def summary(self):
        loss = ((self.sent - self.received) / self.sent) * 100
        return {
            "sent": self.sent,
            "received": self.received,
            "loss": loss,
            "min": min(self.rtts) if self.rtts else None,
            "avg": sum(self.rtts) / len(self.rtts) if self.rtts else None,
            "max": max(self.rtts) if self.rtts else None
        }
