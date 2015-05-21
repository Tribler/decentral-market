from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


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
        self.transport.write("whatsup mang", (self.host, self.port))


senderObj = UdpSender("meh", "224.0.0.1", 8005)

reactor.listenMulticast(8005, senderObj, listenMultiple=True)
# reactor.run()