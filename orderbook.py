import datetime

bids = []
asks = []
message_id = 0

def create_offer(id, type=None, price=None, quantity=None, timeout=None, trade_id=None):
    '''
    Creates an offer.

    Offer can have 5 types: ask, bid, trade, cancel, greeting.
    Depending on the type of offer, an argument might be mandatory.
    '''

    offer = {
        "id": id,
        "message-id": message_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "type": type,
    }

    if type in ["ask", "bid"]:
        offer.update({
            "price": price,
            "quantity": quantity,
            "timeout": timeout
        })
    elif type == "trade":
        offer.update({
            "quantity": quantity,
            "trade-id": trade_id,
        })
    elif type == "cancel":
        offer.update({
            "trade-id": trade_id,
        })

    return offer


def match_bid(bid):
    ask = lowest_ask()
    return ask if ask['price'] <= bid['price'] else None


def lowest_ask(offers=offers):
    return min(asks, key=lambda x: x['price'])
