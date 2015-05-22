import json
import random

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from crypto import get_public_bytestring
from orderbook import (match_incoming_ask, match_incoming_bid,
        get_bids, get_asks, get_own_bids, get_own_asks,
        trades, offers, get_offer, remove_offer,
        trade_offer, create_confirm, create_cancel)


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
            handle_data(real_data)
            self.relay_message(data)
            self.history[real_data['message-id']] = True
            print_all_offers()
        else:
            print "duplicate message received. ID:%d" % real_data['message-id']

    def relay_message(self, message):
        gossip_targets = random.sample(self.peers, 2)
        for address in gossip_targets:
            self.transport.write(message, (address, int(self.peers[address])))

    def load_peers(self):
        with open("peerlist.txt") as f:
            for line in f:
                (address, port) = line.split(':')
                self.peers[address] = port


def handle_data(data):
    try:
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
        elif data['type'] == 'cancel':
            response_dict = handle_cancel(data)
        return json.dumps(response_dict), data['type']
    except ValueError, e:
        print e.message
        return e.message


def handle_ask(ask):
    bid = match_incoming_ask(ask)
    if bid:
        return trade_offer(ask, bid)
    else:
        offers.append(ask)
        return 'Your ask got processed!'


def handle_bid(bid):
    ask = match_incoming_bid(bid)
    if ask:
        return trade_offer(bid, ask)
    else:
        offers.append(bid)
        return "Your bid got processed!"


def handle_trade(trade):
    id, trade_id = get_public_bytestring(), trade['trade-id']
    offer = get_offer(id=id, message_id=trade_id)
    if offer:
        remove_offer(id=id, message_id=trade_id)
        trades.append(offer)
        return create_confirm(recipient=trade['id'], trade_id=trade_id)
    else:
        return create_cancel(recipient=trade['id'], trade_id=trade_id)


def handle_confirm(confirm):
    offer = remove_offer(id=confirm['id'], message_id=confirm['trade_id'])
    trades.append(offer)
    return 'Trade succesful!'


def handle_cancel(cancel):
    return 'Trade cancelled'


def handle_greeting(greeting):
    return 'Hi!'

reactor.listenMulticast(8005, UdpReceive("listener1"), listenMultiple=True)
# reactor.listenMulticast(8005, UdpSender("listener2"), listenMultiple=True)
reactor.run()
