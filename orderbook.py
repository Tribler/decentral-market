import datetime

from crypto import retrieve_key

own_bids = []
own_asks = []

bids = []
asks = []
trades = []

message_id = 0


def create_ask(id, price, quantity, timeout):
    message = create_msg(options={
            'type': 'ask',
            'price': price,
            'quantity': quantity,
            'timeout': timeout
        })
    own_asks.append(message)
    return message


def create_bid(id, price, quantity, timeout):
    message = create_msg(options={
            'type': 'bid',
            'price': price,
            'quantity': quantity,
            'timeout': timeout
        })
    own_bids.append(message)
    return message


def create_trade(id, quantity, trade_id):
    return create_msg(options={
            "quantity": quantity,
            "trade-id": trade_id,
        })


def create_confirm(id, trade_id):
    return create_msg(options={
        "trade-id": trade_id,
    })

def create_greeting(id):
    return create_msg(id, type='greeting')


def create_msg(options=None):
    '''
    Standard for message passing.

    All messages contain an id, a message-id and a timestamp.

    id: public key
    message-id: global incremented value
    timestamp: current time in iso format
    '''

    if options is None:
        options = {}

    global message_id

    message = {
        "id": retrieve_key(),
        "message-id": message_id,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    message.update(options)

    message_id = message_id + 1

    return message


def trade_offer(their_offer, own_offer):
    '''
    Create a trade message replying to one of their offers.
    '''
    if their_offer['type'] == 'bid':
        own_asks.remove(own_offer)
    else:
        own_bids.remove(own_offer)
    trades.append(own_offer)

    return create_trade(
        id=own_offer['id'],
        quantity=own_offer['quantity'],
        trade_id="{};{}".format(their_offer['id'], their_offer['message-id'])
    )


def match_bid(bid, asks=asks):
    '''Match a bid of your own with the lowest ask from the other party.'''
    matching_asks = filter(lambda ask: ask['price'] <= bid['price'], asks)
    return lowest_offer(matching_asks)


def match_incoming_bid(bid):
    '''Match a bid from the other party with your own asks.'''
    matching_asks = filter(lambda ask: ask['price'] >= bid['price'], asks)
    return highest_offer(matching_asks)


def match_ask(ask, bids=bids):
    '''Match an ask of your own with the highest bid from the other party.'''
    matching_bids = filter(lambda bid: bid['price'] >= ask['price'], bids)
    return highest_offer(matching_bids)


def match_incoming_ask(ask):
    '''Match an ask from the other party with your own bids'''
    matching_bids = filter(lambda bid: bid['price'] <= ask['price'], own_bids)
    return lowest_offer(matching_bids)


def lowest_offer(offers):
    return min(offers, key=lambda x: x['price']) if offers else None


def highest_offer(offers):
    return max(offers, key=lambda x: x['price']) if offers else None


def remove_offer(id, message_id, offers):
    for offer in offers:
        if offers['id'] == id and offers['message-id'] == message_id:
            offers.remove(offer)
