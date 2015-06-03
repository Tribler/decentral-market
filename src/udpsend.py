import datetime
import json
from time import sleep

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from orderbook import create_ask, create_bid, create_greeting


class UdpSender(DatagramProtocol):

    def __init__(self, name, host, port):
        self.name = name
        self.loopObj = None
        self.host = host
        self.port = port

    def startProtocol(self):
        self.send_message()

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        pass

    def send_message(self):

        now = datetime.datetime.now()
        next_year = now.replace(year=now.year + 1).isoformat()
        last_year = now.replace(year=now.year - 1).isoformat()

        print next_year


        msg = create_greeting()
        msg = json.dumps(msg)
        self.transport.write(msg, (self.host, self.port))
        sleep(0.3)
        offer = create_bid(price='4', quantity='3', timeout=last_year)
        offer = json.dumps(offer)
        self.transport.write(offer, (self.host, self.port))
        sleep(0.3)
        msg = create_ask(price='6', quantity='6', timeout=next_year)
        msg = json.dumps(msg)
        self.transport.write(msg, (self.host, self.port))
        sleep(0.3)
        sleep(0.3)
        offer = create_bid(price='4', quantity='6', timeout=last_year)
        offer = json.dumps(offer)
        self.transport.write(offer, (self.host, self.port))
        msg = create_ask(price='2', quantity='6', timeout=next_year)
        msg = json.dumps(msg)
        self.transport.write(msg, (self.host, self.port))


senderObj = UdpSender("meh", "224.0.0.1", 8005)

reactor.listenMulticast(8005, senderObj, listenMultiple=True)
# reactor.run()
