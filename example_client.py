from datetime import datetime

from orderbook import create_ask, create_bid
from trade_client import send_offer, handle_response

ip = raw_input("Enter ip address: ")
port = raw_input("Enter port nr: ")

while True:
    o = raw_input("Ask (1) or bid (2)? ")
    if o == "1":
        offer = create_ask(price='3', quantity='6', timeout=datetime.now().isoformat())

        print "Offer: {}".format(str(offer))
        response = send_offer(ip, int(port), offer)
        print "Response: {}".format(str(response))

        print "\n"

        offer = handle_response(response)
        if offer:
            print "Offer: {}".format(str(offer))
            response = send_offer(ip, int(port), offer)
            print "Response: {}".format(str(response))
    elif o == "2":
        offer = create_bid(price='4', quantity='3', timeout=datetime.now().isoformat())
        print "Offer: {}".format(str(offer))
        response = send_offer(ip, int(port), offer)
        print "Response: {}".format(str(response))

        offer = handle_response(response)
        if offer:
            print "Offer: {}".format(str(offer))
            response = send_offer(ip, int(port), offer)
            print "Response: {}".format(str(response))
