import datetime

from crypto import get_public_bytestring

offers = []
trades = []

message_id = 0


def create_ask(price, quantity, timeout):
    message = create_msg(options={
        'type': 'ask',
        'price': price,
        'quantity': quantity,
        'timeout': timeout
    })
    offers.append(message)
    return message


def create_bid(price, quantity, timeout):
    message = create_msg(options={
        'type': 'bid',
        'price': price,
        'quantity': quantity,
        'timeout': timeout
    })
    offers.append(message)
    return message


def create_trade(recipient, quantity, trade_id):
    return create_msg(options={
        'recipient': recipient,
        'type': 'trade',
        'quantity': quantity,
        'trade-id': trade_id,
    })


def create_confirm(recipient, trade_id):
    return create_msg(options={
        'recipient': recipient,
        'type': 'confirm',
        'trade-id': trade_id,
    })


def create_cancel(recipient, trade_id):
    return create_msg(options={
        'recipient': recipient,
        'type': 'cancel',
        'trade-id': trade_id,
    })


def create_greeting():
    return create_msg(options={
        'type': 'greeting'
    })


def create_greeting_response(peers):
    return create_msg(options={
        'type': 'greeting_response',
        'peerlist': peers
    })


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
        "id": get_public_bytestring(),
        "message-id": message_id,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    message.update(options)

    message_id = message_id + 1

    return message


def trade_offer(their_offer, own_offer):
    '''Create a trade message replying to one of their offers.'''
    return create_trade(
        recipient=their_offer['id'],
        quantity=own_offer['quantity'],
        trade_id=their_offer['message-id'],
    )


def get_offer(id, message_id):
    for offer in offers:
        if offer['id'] == id and offer['message-id'] == message_id:
            return offer
    return None


def clean_offers(f):
    def func_wrapper(*args, **kwargs):
        for offer in offers:
            if offer['timeout'] < datetime.datetime.now():
                offers.remove(offer)
        return f(*args, **kwargs)
    return func_wrapper


@clean_offers
def get_asks():
    return filter(lambda offer:
                offer['type'] == 'ask' and
                offer['id'] != get_public_bytestring(),
            offers)


@clean_offers
def get_own_asks():
    return filter(lambda offer:
                offer['type'] == 'ask' and
                offer['id'] == get_public_bytestring(),
            offers)


@clean_offers
def get_bids():
    return filter(lambda offer:
                offer['type'] == 'bid' and
                offer['id'] != get_public_bytestring(),
            offers)


@clean_offers
def get_own_bids():
    return filter(lambda offer:
                offer['type'] == 'bid' and
                offer['id'] == get_public_bytestring(),
            offers)


@clean_offers
def match_bid(bid):
    '''Match a bid of your own with the lowest ask from the other party.'''
    matching_asks = filter(lambda ask: ask['price'] <= bid['price'], get_asks())
    return lowest_offer(matching_asks)


@clean_offers
def match_incoming_bid(bid):
    '''Match a bid from the other party with your own asks.'''
    matching_asks = filter(lambda ask: ask['price'] >= bid['price'], get_own_asks())
    return highest_offer(matching_asks)


@clean_offers
def match_ask(ask):
    '''Match an ask of your own with the highest bid from the other party.'''
    matching_bids = filter(lambda bid: bid['price'] >= ask['price'], get_bids())
    return highest_offer(matching_bids)


@clean_offers
def match_incoming_ask(ask):
    '''Match an ask from the other party with your own bids'''
    matching_bids = filter(lambda bid: bid['price'] <= ask['price'], get_own_bids())
    return lowest_offer(matching_bids)


def lowest_offer(offers):
    return min(offers, key=lambda x: x['price']) if offers else None


def highest_offer(offers):
    return max(offers, key=lambda x: x['price']) if offers else None


def remove_offer(id, message_id):
    offer = get_offer(id, message_id)
    if offer:
        offers.remove(offer)
    return offer
