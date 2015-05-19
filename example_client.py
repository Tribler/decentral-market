from datetime import datetime

from orderbook import create_msg
from trade_client import send_offer, handle_response

port = raw_input("Enter port nr: ")
for x in xrange(3):
    offer = create_msg(1, type="ask", price=3, quantity="4", timeout=datetime.now().isoformat())

    print "Offer: {}".format(str(offer))
    response = send_offer('localhost', int(port), offer)
    print "Response: {}".format(str(response))

    print "\n"

    offer = handle_response(response)
    if offer:
        print "Offer: {}".format(str(offer))
        response = send_offer('localhost', int(port), offer)
        print "Response: {}".format(str(response))
