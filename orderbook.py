import datetime

own_bids = []
own_asks = []
bids = []
asks = []
message_id = 0


def create_msg(id, type=None, price=None, quantity=None, timeout=None, trade_id=None):
    '''
    Standard for message passing.

    Message can have 5 types: ask, bid, trade, cancel, greeting.
    Depending on the type of message, an argument might be mandatory.
    '''

    message = {
        "id": id,
        "message-id": message_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "type": type,
    }

    if type in ["ask", "bid"]:
        message.update({
            "price": price,
            "quantity": quantity,
            "timeout": timeout
        })
        if type == "ask":
            own_asks.append(message)
        else:
            own_bids.append(message)
    elif type == "trade":
        message.update({
            "quantity": quantity,
            "trade-id": trade_id,
        })
    elif type == "cancel":
        message.update({
            "trade-id": trade_id,
        })

    return message


def match_incoming_bid(bid):
    return match_bid(bid, own_asks)


def match_bid(bid, asks=asks):
    ask = lowest_ask(asks)
    return ask if ask and ask['price'] <= bid['price'] else None


def match_incoming_ask(ask):
    return match_ask(ask, own_bids)


def match_ask(ask, bids=bids):
    bid = highest_bid(bids)
    return bid if bid and bid['price'] >= ask['price'] else None


def lowest_ask(asks=asks):
    return min(asks, key=lambda x: x['price']) if asks else None


def highest_bid(bids=bids):
    return max(bids, key=lambda x: x['price']) if bids else None
