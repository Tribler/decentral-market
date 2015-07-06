import json

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from orderbook import create_ask


class MessageSender(DatagramProtocol):
    '''Sole purpose is to send one message'''

    def __init__(self, name, msg):
        self.name = name
        self.msg = msg
        self.host = '224.0.0.1'
        self.port = 8005

    def startProtocol(self):
        self.send_message(self.msg)

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        pass

    def send_message(self, msg):
        msg = json.dumps(msg)
        self.transport.write(msg, (self.host, self.port))
        print "Transported message"


def createask(ip='224.0.0.1'):
    ask = create_ask(1, 1)
    sender = MessageSender("bla", ask)
    reactor.listenMulticast(8005, sender, listenMultiple=True)
