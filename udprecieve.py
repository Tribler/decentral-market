from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import time, random


class UdpSender(DatagramProtocol):
    def __init__(self, name):
        self.name = name
        self.message_count = 0
        self.history = {}
        self.peers = {}

    def startProtocol(self):
        pass

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        now = time.localtime(time.time())
        time_str = str(time.strftime("%y/%m/%d %H:%M:%S", now))
        print "%s received %r from %s:%d at %s" % (self.name, data, host, port, time_str)
        if not self.history[data]:
            self.relay_message(data)
            self.history[data] = True

    def send_message(self):
        message = "%d whatsup mang" % self.message_count
        if not self.history[message]:
            self.transport.write(message, ("224.0.0.1", 8005))
            self.history[message] = True

    def relay_message(self, message):
        gossip_targets = random.sample(self.peers, 4)
        for address in gossip_targets:
            self.transport.write(message, (address, self.peers[address]))

    def load_peers(self):
        with open("peerlist.txt") as f:
            for line in f:
                (address, port) = line.split()
                self.peers[address] = port

reactor.listenMulticast(8005, UdpSender("listener1"), listenMultiple=True)
reactor.listenMulticast(8005, UdpSender("listener2"), listenMultiple=True)
reactor.run()