import datetime
import json
import os

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, threads
from twisted.python import threadable
from orderbook import create_ask, create_bid, create_greeting


class UdpSender(DatagramProtocol):

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

    def startProtocol(self):
        pass

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        pass

    def send_message(self, price, qty, msgtype):
        now = datetime.datetime.now()
        next_year = now.replace(year=now.year + 1).isoformat()

        if msgtype == 'G':
            msg = create_greeting()
            msg = json.dumps(msg)
            self.transport.write(msg, (self.host, self.port))
        else:
            if msgtype == 'A':
                msg = create_ask(price, qty, timeout=next_year)
            elif msgtype == 'B':
                msg = create_bid(price, qty, timeout=next_year)
            msg = json.dumps(msg)
            self.transport.write(msg, (self.host, self.port))
            print "Transported message"


def create_peer(id):
    senderObj = UdpSender(id, "224.0.0.1", 8005)
    reactor.listenMulticast(8005, senderObj, listenMultiple=True)
    return senderObj

