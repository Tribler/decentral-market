from datetime import datetime

from trade_server import create_server
from orderbook import create_bid, own_bids

server = create_server()
print server.server_address


# Create 3 bids with prices 6, 3, and 2.
create_bid(1234, price=6, quantity=4, timeout=datetime.now().isoformat())
create_bid(1234, price=3, quantity=4, timeout=datetime.now().isoformat())
create_bid(1234, price=2, quantity=4, timeout=datetime.now().isoformat())

print "\n".join(str(bid) for bid in own_bids)
try:
    while True:
        pass
except KeyboardInterrupt:
    print "Shutting down server..."
    server.server_close()
    print "Server shut down. Goodbye."
