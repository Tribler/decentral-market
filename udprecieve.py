from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import time, random, json
from orderbook import asks, bids, match_incoming_ask, match_incoming_bid, trade_offer
from orderbook import create_confirm


class UdpSender(DatagramProtocol):
    def __init__(self, name):
        self.name = name
        self.message_count = 0
        self.history = {}
        self.peers = {}

    def startProtocol(self):
        self.load_peers()
        pass

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        real_data = json.loads(data)
        now = time.localtime(time.time())
        time_str = str(time.strftime("%H:%M:%S", now))
        print "%s received %r from %s:%d at %s" % (self.name, data, host, port, time_str)
        if not real_data['message-id'] in self.history:
            handle_data(data)
            self.relay_message(data)
            self.history[real_data['message-id']] = True

    def send_message(self):
        message = "%d whatsup mang" % self.message_count
        if not self.history[message]:
            self.transport.write(message, ("224.0.0.1", 8005))
            self.history[message] = True

    def relay_message(self, message):
        gossip_targets = random.sample(self.peers, 2)
        print gossip_targets
        for address in gossip_targets:
            self.transport.write(message, (address, int(self.peers[address])))

    def load_peers(self):
        with open("peerlist.txt") as f:
            for line in f:
                (address, port) = line.split(':')
                self.peers[address] = port


def handle_data(data):
    try:
        data = json.loads(data)
        if data['type'] == 'ask':
            response_dict = handle_ask(data)
        elif data['type'] == 'bid':
            response_dict = handle_bid(data)
        elif data['type'] == 'greeting':
            response_dict = handle_greeting(data)
        elif data['type'] == 'trade':
            response_dict = handle_trade(data)
        elif data['type'] == 'confirm':
            response_dict = handle_confirm(data)
        return json.dumps(response_dict), data['type']
    except ValueError, e:
        print e.message
        return e.message


def handle_ask(ask):
    bid = match_incoming_ask(ask)
    if bid:
        return trade_offer(ask, bid)
    else:
        asks.append(ask)
        return 'Your ask got processed!'


def handle_bid(bid):
    ask = match_incoming_bid(bid)
    if ask:
        return trade_offer(bid, ask)
    else:
        bids.append(bid)
        return "Your bid got processed!"


def handle_trade(trade):
    return 'Trade succesful!'


def handle_confirm(confirm):
    return 'Trade succesful!'


def handle_greeting(greeting):
    return 'Hi!'


def handle_trade(trade):
    # id is not yet properly implemented so we use this ugly hack for now

    # Cancel messages are not yet implemented. See issue #7.

    return create_confirm(
        trade_id=trade['trade-id']
    )

reactor.listenMulticast(8005, UdpSender("listener1"), listenMultiple=True)
#reactor.listenMulticast(8005, UdpSender("listener2"), listenMultiple=True)
reactor.run()