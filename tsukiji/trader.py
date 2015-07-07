# -*- coding: utf-8
import json
from twisted.protocols import basic
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, stdio

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
        except ValueError:
            print 'Data received: {}'.format(data)

    def relay_message(self, message):
        for address in self.peers:
            self.transport.write(message, (address, int(self.peers[address])))

    def read_peerlist(self):
        with open("peerlist.txt") as f:
            return dict(line.strip().split(':') for line in f.readlines())

    def add_to_peerlist(self, host, port):
        if not host == self.transport.getHost().host:
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

    def send_offer(self, offer):
        offer = json.dumps(offer)
        self.relay_message(offer)

    def send_greeting(self):
        greeting = json.dumps(greeting)
        self.relay_message(greeting)


class Repl(basic.LineReceiver):
    '''Console input for controlling Tsukiji.'''
    delimiter = '\n'

    def connectionMade(self):
        self.sendLine('tsukiji console. Type \'help\' for more info.')
        self.trader = Trader('tsukiji')
        reactor.listenMulticast(8005, self.trader, listenMultiple=True)

    def lineReceived(self, line):
        if not line: return

        command_parts = line.split()
        command = command_parts[0]
        args = command_parts[1:]

        try:
            method = getattr(self, 'do_' + command)
        except AttributeError, e:
            self.sendLine('Error: no such command.')
        else:
            try:
                method(*args)
            except Exception, e:
                self.sendLine('Error: ' + str(e))

    def do_help(self, command=None):
        """help [command]: List commands, or show help on the given command."""
        if command:
            self.sendLine(getattr(self, 'do_' + command).__doc__)
        else:
            commands = [cmd[3:] for cmd in dir(self) if cmd.startswith('do_')]
            self.sendLine("Valid commands: " +" ".join(commands))


    def do_ask(self, price=None, quantity=None):
        '''ask [price, quantity]: Create and post an ask.'''
        ask = create_ask(float(price), float(quantity))
        self.trader.send_offer(ask)

    def do_bid(self, price=None, quantity=None):
        '''bid [price, quantity]: Create and post a bid.'''
        bid = create_bid(float(price), float(quantity))
        self.trader.send_offer(bid)

    def do_greeting(self):
        '''greeting: greet everybody in your peerlist.'''
        print 'Saying hello to everybody.'
        self.trader.send_greeting()

    def do_offers(self):
        '''offers: List all offers'''
        print_all_offers()

    def do_quit(self):
        '''quit: Quit this session.'''
        self.sendLine('さよなら')
        self.transport.loseConnection()

    def connectionLost(self, reason):
        reactor.stop()


if __name__ == '__main__':
    stdio.StandardIO(Repl())
    reactor.run()
