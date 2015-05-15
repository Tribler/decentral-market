import datetime

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


def match_bid(bid):
    ask = lowest_ask()
    return ask if ask['price'] <= bid['price'] else None


def match_ask(ask):
    bid = highest_bid()
    return bid if bid['price'] >= ask['price'] else None


def lowest_ask(asks=asks):
    return min(asks, key=lambda x: x['price'])


def highest_bid(bids=bids):
    return max(bids, key=lambda x: x['price'])
