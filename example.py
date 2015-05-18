from datetime import datetime

from trade_server import create_server
from orderbook import create_bid, own_bids, bids, asks, own_bids, own_asks, trades

def offer_to_string(offer):
    s = "{\n"
    for k, v in offer.iteritems():
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
    '''.format(*[offers_to_string(o) for o in (asks, bids, own_asks, own_bids)])


server = create_server()
print server.server_address


# Create 3 bids with prices 6, 3, and 2.
create_bid(1234, price=6, quantity=4, timeout=datetime.now().isoformat())
create_bid(1234, price=3, quantity=4, timeout=datetime.now().isoformat())
create_bid(1234, price=2, quantity=4, timeout=datetime.now().isoformat())

print_all_offers()
try:
    while True:
        pass
except KeyboardInterrupt:
    print "Shutting down server..."
    server.server_close()
    print "Server shut down. Goodbye."



print_all_offers()
