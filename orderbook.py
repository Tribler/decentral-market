import datetime

own_bids = []
own_asks = []
bids = []
asks = []
message_id = 0


def create_ask(id, price, quantity, timeout):
    return create_msg(id, type='ask', price=price, quantity=quantity, timeout=timeout)


def create_bid(id, price, quantity, timeout):
    return create_msg(id, type='bid', price=price, quantity=quantity, timeout=timeout)


def create_trade(id, quantity, trade_id):
    return create_msg(id, type='trade', quantity=quantity, trade_id=trade_id)


def create_greeting(id):
    return create_msg(id, type='greeting')


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


def match_bid(bid):
    '''Match a bid of your own with the lowest ask from the other party.'''
    ask = lowest_ask(asks)
    return ask if ask and ask['price'] <= bid['price'] else None


def match_ask(ask):
    '''Match an ask of your own with the highest bid from the other party.'''
    bid = highest_bid(bids)
    return bid if bid and bid['price'] >= ask['price'] else None


def lowest_ask(asks=asks):
    return min(asks, key=lambda x: x['price']) if asks else None


def highest_bid(bids=bids):
    return max(bids, key=lambda x: x['price']) if bids else None
