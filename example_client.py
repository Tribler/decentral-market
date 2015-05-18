from datetime import datetime

from orderbook import create_msg
from trade_client import send_offer

port = raw_input("Enter port nr: ")
offer = create_msg(1, type="ask", price=3, quantity="4", timeout=datetime.now().isoformat())

print "Offer: {}".format(str(offer))

send_offer('localhost', int(port), offer)
