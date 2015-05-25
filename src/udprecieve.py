from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import random, json
from orderbook import match_incoming_ask, match_incoming_bid, trade_offer, create_confirm, get_bids, get_asks, get_own_bids, get_own_asks, trades, create_greeting_response
from orderbook import offers, get_offer

# Printing functions for testing
def offer_to_string(offer):
    s = "{\n"
    for k, v in offer.iteritems():
        if k == 'id':
            v = v.split('\n')[1][:20] + '...'
        s += "\t{}: {}\n".format(k, v)
    s += "    }"
    return s


def offers_to_string(offers):
    return '\n    '.join(offer_to_string(offer) for offer in offers)


def print_all_offers():

    print '''
    Bids
    =========
    {}

    Asks
    ========
    {}

    Own bids
    ========
    {}

    Own Asks
    ========
    {}

    Trades
    ========
    {}
    '''.format(*[offers_to_string(o) for o in (get_bids(), get_asks(), get_own_bids(), get_own_asks(), trades)])


class UdpReceive(DatagramProtocol):
    def __init__(self, name):
        self.name = name
        self.history = {}
        self.peers = {}

    def startProtocol(self):
        self.load_peers()
        pass

    def stopProtocol(self):
        pass

    def datagramReceived(self, data, (host, port)):
        real_data = json.loads(data)

        if not real_data['message-id'] in self.history:
            self.handle_data(data, host, port)
            self.relay_message(data)
            self.history[real_data['message-id']] = True
            print_all_offers()
        else:
            print "duplicate message received. ID:%d" % real_data['message-id']

    def relay_message(self, message):
        gossip_targets = random.sample(self.peers, 2)
        #print gossip_targets
        for address in gossip_targets:
            self.transport.write(message, (address, int(self.peers[address])))

    def direct_message(self, message, host, port):
        self.transport.write(message, (host, port))

    def load_peers(self):
        self.peers = self.read_peerlist()

    def read_peerlist(self):
        peer_dict = {}
        with open("peerlist.txt") as f:
            for line in f:
                (address, port) = line.split(':')
                peer_dict[address] = port
        return peer_dict

    def add_to_peerlist(self, host, port):
        with open("peerlist.txt", "a") as f:
            new_peer = host + ":" + str(port) + "\n"
            f.write(new_peer)

    def handle_data(self, data, host='127.0.0.1', port=8005):
        try:
            data = json.loads(data)
            if data['type'] == 'ask':
                response_dict = self.handle_ask(data)
            elif data['type'] == 'bid':
                response_dict = self.handle_bid(data)
            elif data['type'] == 'greeting':
                response_dict = self.handle_greeting(host, port)
            elif data['type'] == 'greeting_response':
                response_dict = self.handle_greeting_response(data)
            elif data['type'] == 'trade':
                response_dict = self.handle_trade(data)
            elif data['type'] == 'confirm':
                response_dict = self.handle_confirm(data)
            return json.dumps(response_dict), data['type']
        except ValueError, e:
            print e.message
            return e.message

    def handle_ask(self, ask):
        bid = match_incoming_ask(ask)
        if bid:
            return trade_offer(ask, bid)
        else:
            offers.append(ask)
            return 'Your ask got processed!'

    def handle_bid(self, bid):
        ask = match_incoming_bid(bid)
        if ask:
            return trade_offer(bid, ask)
        else:
            offers.append(bid)
            return "Your bid got processed!"

    def handle_trade(self, trade):
        id, message_id = trade['trade-id'].split(';')
        offer = get_offer(id, message_id)
        if offer:
            # Send a confirm
            pass
        else:
            # Send a cancel
            pass
        return 'Trade succesful!'

    def handle_confirm(self, confirm):
        return 'Trade succesful!'

    def handle_greeting(self, host, port):
        peer_list = self.read_peerlist()
        self.add_to_peerlist(host, port)
        msg = create_greeting_response(peer_list)
        msg = json.dumps(msg)
        self.direct_message(msg, host, port)
        return 'Peerlist sent'

    def handle_greeting_response(self, data):
        self.peers = data['peerlist']
        print self.peers
        return 'Peers added'

reactor.listenMulticast(8005, UdpReceive("listener1"), listenMultiple=True)
# reactor.listenMulticast(8005, UdpSender("listener2"), listenMultiple=True)
reactor.run()