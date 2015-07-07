# -*- coding: utf-8
from twisted.protocols import basic
from twisted.internet import reactor, stdio

from trader import Trader
import orderbook as ob
from utils import print_all_offers


class Repl(basic.LineReceiver):
    '''Console input for controlling Tsukiji.'''
    delimiter = '\n'

    def connectionMade(self):
        self.sendLine('tsukiji console. Type \'help\' for more info.')
        self.trader = Trader('tsukiji')
        reactor.listenMulticast(8005, self.trader, listenMultiple=True)

    def lineReceived(self, line):
        if not line:
            return

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
            self.sendLine("Valid commands: " + " ".join(commands))

    def do_ask(self, price=None, quantity=None):
        '''ask [price, quantity]: Create and post an ask.'''
        ask = ob.create_ask(float(price), float(quantity))
        self.trader.send_offer(ask)

    def do_bid(self, price=None, quantity=None):
        '''bid [price, quantity]: Create and post a bid.'''
        bid = ob.create_bid(float(price), float(quantity))
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
