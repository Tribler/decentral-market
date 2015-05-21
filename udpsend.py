from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from orderbook import create_ask, create_bid
import json

class UdpSender(DatagramProtocol):

    def __init__(self, name, host, port):
        self.name = name
        self.loopObj = None
        self.host = host
        self.port = port

    def startProtocol(self):
        self.send_message()
        #self.loopObj = LoopingCall(self.sendHeartBeat)
        #self.loopObj.start(2, now=False)

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)

    def send_message(self):
        msg = create_ask(price='3', quantity='6', timeout=1)
        msg = json.dumps(msg)
        self.transport.write(msg, (self.host, self.port))


senderObj = UdpSender("meh", "224.0.0.1", 8005)

reactor.listenMulticast(8005, senderObj, listenMultiple=True)
# reactor.run()