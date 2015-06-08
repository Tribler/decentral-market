from nose import with_setup

from tsukiji import orderbook as ob
from tsukiji.crypto import get_public_bytestring


import datetime
now = datetime.datetime.now()
next_year = now.replace(year=now.year + 1)
last_year = now.replace(year=now.year - 1)
public_id = get_public_bytestring()


def clear_orderbook():
    ob.message_id = 0
    ob.offers = []
    ob.trades = []


@with_setup(clear_orderbook)
def test_create_msg():
    message = ob.create_msg()
    assert type(message) == dict
    assert message['id'] == public_id
    assert message['message-id'] == 0


@with_setup(clear_orderbook)
def test_create_msg_incrementing_message_id():
    m1 = ob.create_msg()
    m2 = ob.create_msg()

    assert m1['message-id'] == 0, 'Expected 0, got {}'.format(m1['message-id'])
    assert m2['message-id'] == 1, 'Expected 1, got {}'.format(m2['message-id'])


@with_setup(clear_orderbook)
def test_create_msg_passing_options():
    options = {
        'hello': 'world',
    }

    message = ob.create_msg(options=options)
    assert 'hello' in message
    assert message['hello'] == 'world'


@with_setup(clear_orderbook)
def test_create_msg_passing_options_overriding_default():
    options = {
        'id': 1234,
    }

    message = ob.create_msg(options=options)
    assert 'id' in message
    assert message['id'] == 1234


@with_setup(clear_orderbook)
def test_create_ask():
    ask = ob.create_ask(1, 1, now)
    assert ask['type'] == 'ask'
    assert ask['price'] == 1
    assert ask['quantity'] == 1
    assert len(ob.offers) == 1


@with_setup(clear_orderbook)
def test_create_bid():
    import datetime
    ask = ob.create_bid(1, 1, datetime.datetime.now())
    assert ask['type'] == 'bid'
    assert ask['price'] == 1
    assert ask['quantity'] == 1
    assert len(ob.offers) == 1


@with_setup(clear_orderbook)
def test_create_trade():
    trade = ob.create_trade('abcd', 1, 1)
    assert trade['type'] == 'trade'
    assert trade['recipient'] == 'abcd'
    assert trade['quantity'] == 1
    assert trade['trade-id'] == 1


@with_setup(clear_orderbook)
def test_create_confirm():
    confirm = ob.create_confirm('abcd', 1)
    assert confirm['type'] == 'confirm'
    assert confirm['recipient'] == 'abcd'
    assert confirm['trade-id'] == 1


@with_setup(clear_orderbook)
def test_create_cancel():
    cancel = ob.create_cancel('abcd', 1)
    assert cancel['type'] == 'cancel'
    assert cancel['recipient'] == 'abcd'
    assert cancel['trade-id'] == 1


@with_setup(clear_orderbook)
def test_create_greeting():
    greeting = ob.create_greeting()
    assert greeting['type'] == 'greeting'


@with_setup(clear_orderbook)
def test_create_greeting_response():
    greeting_response = ob.create_greeting_response(['abcd', 'efgh'])
    assert greeting_response['type'] == 'greeting_response'
    assert greeting_response['peerlist'] == ['abcd', 'efgh']


@with_setup(clear_orderbook)
def test_get_offer():
    ask = ob.create_ask(1, 1, next_year)
    offer = ob.get_offer(public_id, 0)
    assert ask == offer, 'Expected {}, got {}'.format(ask, offer)

@with_setup(clear_orderbook)
def test_get_offer_empty_orderbook():
    offer = ob.get_offer(1, 1)
    assert offer is None, 'Expected None, got {}'.format(offer)

@with_setup(clear_orderbook)
def test_clean_offers():
    ob.create_ask(1,1,last_year)
    mock_function = lambda *x: x
    ob.clean_offers(mock_function)()
    assert len(ob.offers) == 0, 'Expected empty list, got {}'.format(ob.offers)
