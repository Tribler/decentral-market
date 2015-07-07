import datetime
import json
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from crypto import get_public_bytestring
from orderbook import (match_incoming_ask, match_incoming_bid,
        trades, offers, get_offer, remove_offer,
        trade_offer, create_confirm, create_cancel, create_greeting_response,
        create_bid, create_ask)
from utils import print_all_offers
from paypal import make_a_payment


class Trader(DatagramProtocol):
    def __init__(self, name):
        self.name = name
        self.history = set()
        self.peers = self.read_peerlist()

    def startProtocol(self):
        pass

    def stopProtocol(self):
        pass

    def datagramReceived(self, raw_data, (host, port)):
        try:
            data = json.loads(raw_data)
            if type(data) is unicode:
                raise ValueError('Data received was a string.')
            id, message_id = data['id'], data['message-id']

            if (id, message_id) not in self.history:
                # Process incoming messages
                self.handle_data(data, host, port)

                # Relay offers
                if data['type'] in ['ask', 'bid']:
                    print_all_offers()
                    self.relay_message(raw_data)

                # Add message to history to eliminate duplicate messages
                self.history.add((id, message_id))
            else:
                print 'Duplicate message received.\n id: {}..., message-id: {}'.format(id[26:50], message_id)
        except ValueError, e:
            print 'Data received: {}'.format(data)

    def relay_message(self, message):
        for address in self.peers:
            self.transport.write(message, (address, int(self.peers[address])))

    def read_peerlist(self):
        with open("peerlist.txt") as f:
            return dict(line.strip().split(':') for line in f.readlines())

    def add_to_peerlist(self, host, port):
        with open("peerlist.txt", "a") as f:
            new_peer = '{}:{}\n'.format(host, port)
            f.write(new_peer)

    def handle_data(self, data, host, port):
        try:
            responses = {
                'ask': self.handle_ask,
                'bid': self.handle_bid,
                'greeting': self.handle_greeting,
                'greeting_response': self.handle_greeting_response,
                'trade': self.handle_trade,
                'confirm': self.handle_confirm,
                'cancel': self.handle_cancel
            }

            if data['type'] == 'greeting':
                response = self.handle_greeting(host, port)
            else:
                response = responses[data['type']](data)
                response = json.dumps(response)
                self.transport.write(response, (host, port))
        except ValueError, e:
            print e.message
            return 'Error: something bad happened'

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
        id, trade_id = get_public_bytestring(), trade['trade-id']
        offer = get_offer(id=id, message_id=trade_id)
        if offer:
            offers.remove(offer)
            trades.append(offer)
            make_a_payment(price=offer['price'])
            return create_confirm(recipient=trade['id'], trade_id=trade_id)
        else:
            return create_cancel(recipient=trade['id'], trade_id=trade_id)

    def handle_confirm(self, confirm):
        offer = remove_offer(id=confirm['id'], message_id=confirm['trade-id'])
        trades.append(offer)
        return 'Trade succesful!'

    def handle_cancel(self, cancel):
        remove_offer(id=cancel['id'], message_id=cancel['trade-id'])
        return 'Trade cancelled'

    def handle_greeting(self, host, port):
        peer_list = self.read_peerlist()
        if host not in peer_list:
            self.add_to_peerlist(host, port)

        msg = create_greeting_response(peer_list)
        msg = json.dumps(msg)
        self.transport.write(msg, (host, port))
        print "Greeting received from " + host + ":" + str(port)
        return 'Peerlist sent'

    def handle_greeting_response(self, data):
        self.peers.update(data['peerlist'])
        for key, value in data['peerlist']:
            self.add_to_peerlist(key, value)
        return 'Peers added'

    def send_demo_offer(self, ask=True):
        if ask:
            offer = create_ask(1, 1)
        else:
            offer = create_bid(1, 1)
        offer = json.dumps(offer)
        self.relay_message(offer)

if __name__ == '__main__':
    trader = Trader("Fan of Tsukiji")
    reactor.listenMulticast(8005, trader, listenMultiple=True)

    choice = raw_input('1 or 2 ')
    if choice == '1':
        trader.send_demo_offer()
    elif choice == '2':
        trader.send_demo_offer(ask=False)

    print_all_offers()
    reactor.run()
