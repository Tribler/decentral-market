import json

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from orderbook import create_ask, create_greeting
from crypto import get_public_bytestring


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
        data = json.loads(data)
        if data['type'] == 'greeting_response':
            print 'Peerlist received: {}'.format(data['peerlist'])
        else:
            print "Response received: {}".format(data)

    def send_message(self, msg):
        msg = json.dumps(msg)
        self.transport.write(msg, (self.host, self.port))
        print "Transported message"


def send_ask(ip='224.0.0.1', message_id=None):
    ask = create_ask(100, 1)
    if message_id:
        ask['message-id'] = message_id
    return MessageSender("bla", ask)


def send_greeting():
    greeting = create_greeting()
    return MessageSender("Michael", greeting)


if __name__ == '__main__':
    choice = raw_input('''Which scenario do you want to run?
    Post a greeting? (g)
    Post an ask? (a)
    Send duplicate messages? (d)
    ''')
    if choice == 'g':
        sender = send_greeting()
    elif choice == 'a':
        sender = send_ask()
    elif choice == 'd':
        sender = send_ask(message_id=100)
        reactor.listenMulticast(8005, send_ask(message_id=100), listenMultiple=True)
    else:
        print 'Naughty Naughty'
        exit()
    print 'Identifier is : {}'.format(get_public_bytestring())
    reactor.listenMulticast(8005, sender, listenMultiple=True)
    reactor.run()
