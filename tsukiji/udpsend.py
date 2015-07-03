import datetime
import json
import random

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, threads
from twisted.python import threadable
from orderbook import create_ask, create_bid, create_greeting


class UdpSender(DatagramProtocol):

    def __init__(self, name, host, port, qty, price, msgtype):
        self.name = name
        self.host = host
        self.port = port
        self.msgtype = msgtype
        self.price = price
        self.qty = qty

    def startProtocol(self):
        self.send_message()

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        pass

    def send_message(self):
        now = datetime.datetime.now()
        next_year = now.replace(year=now.year + 1).isoformat()

        if self.msgtype == 'G':
            msg = create_greeting()
            msg = json.dumps(msg)
            self.transport.write(msg, (self.host, self.port))
        else:
            if self.msgtype == 'A':
                msg = create_ask(self.price, self.qty, timeout=next_year)
            elif self.msgtype == 'B':
                msg = create_bid(self.price, self.qty, timeout=next_year)
            msg = json.dumps(msg)
            self.transport.write(msg, (self.host, self.port))
            print "Transported message"


def create_peer(id, qty, price, msgtype):
    senderObj = UdpSender(id, "224.0.0.1", 8005, qty, price, msgtype)
    senderObj.send_message()
    reactor.listenMulticast(8005, senderObj, listenMultiple=True)


def createask():
    obj = UdpSender("bla", "224.0.0.1", 8005, 1, random.randint(1, 5), 'A')
    reactor.listenMulticast(8005, obj, listenMultiple=True)


def createbid():
    obj = UdpSender("bla", "224.0.0.1", 8005, 1, random.randint(1, 5), 'B')
    reactor.listenMulticast(8005, obj, listenMultiple=True)