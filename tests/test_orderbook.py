from unittest import TestCase

from tsukiji import orderbook as ob
from tsukiji.crypto import get_public_bytestring


import datetime
now = datetime.datetime.now()
next_year = now.replace(year=now.year + 1)
last_year = now.replace(year=now.year - 1)
public_id = get_public_bytestring()


class OrderBookTest(TestCase):
    def setUp(self):
        '''Clean the orderbook before every test.'''
        ob.message_id = 0
        ob.offers = []
        ob.trades = []

    def test_create_msg(self):
        message = ob.create_msg()
        assert type(message) == dict
        assert message['id'] == public_id
        assert message['message-id'] == 0

    def test_create_msg_incrementing_message_id(self):
        m1 = ob.create_msg()
        m2 = ob.create_msg()

        assert m1['message-id'] == 0, 'Expected 0, got {}'.format(m1['message-id'])
        assert m2['message-id'] == 1, 'Expected 1, got {}'.format(m2['message-id'])

    def test_create_msg_passing_options(self):
        options = {
            'hello': 'world',
        }

        message = ob.create_msg(options=options)
        assert 'hello' in message
        assert message['hello'] == 'world'

    def test_create_msg_passing_options_overriding_default(self):
        options = {
            'id': 1234,
        }

        message = ob.create_msg(options=options)
        assert 'id' in message
        assert message['id'] == 1234

    def test_create_ask(self):
        ask = ob.create_ask(1, 1, now)
        assert ask['type'] == 'ask'
        assert ask['price'] == 1
        assert ask['quantity'] == 1
        assert len(ob.offers) == 1

    def test_create_bid(self):
        import datetime
        ask = ob.create_bid(1, 1, datetime.datetime.now())
        assert ask['type'] == 'bid'
        assert ask['price'] == 1
        assert ask['quantity'] == 1
        assert len(ob.offers) == 1

    def test_create_trade(self):
        trade = ob.create_trade('abcd', 1, 1)
        assert trade['type'] == 'trade'
        assert trade['recipient'] == 'abcd'
        assert trade['quantity'] == 1
        assert trade['trade-id'] == 1

    def test_create_confirm(self):
        confirm = ob.create_confirm('abcd', 1)
        assert confirm['type'] == 'confirm'
        assert confirm['recipient'] == 'abcd'
        assert confirm['trade-id'] == 1

    def test_create_cancel(self):
        cancel = ob.create_cancel('abcd', 1)
        assert cancel['type'] == 'cancel'
        assert cancel['recipient'] == 'abcd'
        assert cancel['trade-id'] == 1

    def test_create_greeting(self):
        greeting = ob.create_greeting()
        assert greeting['type'] == 'greeting'

    def test_create_greeting_response(self):
        greeting_response = ob.create_greeting_response(['abcd', 'efgh'])
        assert greeting_response['type'] == 'greeting_response'
        assert greeting_response['peerlist'] == ['abcd', 'efgh']

    def test_get_offer(self):
        ask = ob.create_ask(1, 1, next_year)
        offer = ob.get_offer(public_id, 0)
        assert ask == offer, 'Expected {}, got {}'.format(ask, offer)

    def test_get_offer_empty_orderbook(self):
        offer = ob.get_offer(1, 1)
        assert offer is None, 'Expected None, got {}'.format(offer)

    def test_clean_offers(self):
        ob.create_ask(1, 1, last_year)
        mock_function = lambda *x: x
        ob.clean_offers(mock_function)()
        assert len(ob.offers) == 0, 'Expected empty list, got {}'.format(ob.offers)

    def test_trade_offer(self):
        ask = ob.create_ask(1, 2, next_year)
        ask['id'] = 1234
        bid = ob.create_ask(1, 1, next_year)
        trade = ob.trade_offer(ask, bid)
        assert trade is not None
        assert trade['recipient'] == 1234
        assert trade['quantity'] == 1
        assert trade['trade-id'] == ask['message-id']

    def test_get_asks_empty(self):
        asks = ob.get_asks()
        assert asks == []

    def test_get_asks(self):
        ask = ob.create_ask(1, 1, next_year)
        ask['id'] = 1234
        asks = ob.get_asks()
        assert asks == [ask], 'Expected {}, got {}'.format([ask], asks)

    def test_get_own_asks_empty(self):
        asks = ob.get_own_asks()
        assert asks == [], 'Expected {}, got {}'.format([], asks)

    def test_get_own_asks(self):
        ask = ob.create_ask(1, 1, next_year)
        asks = ob.get_own_asks()
        assert asks == [ask], 'Expected {}, got {}'.format([ask], asks)

    def test_get_bids_empty(self):
        bids = ob.get_bids()
        assert bids == [], 'Expected {}, got {}'.format([], bids)

    def test_get_bids(self):
        bid = ob.create_bid(1, 1, next_year)
        bid['id'] = 1234
        bids = ob.get_bids()
        assert bids == [bid], 'Expected {}, got {}'.format([bid], bids)

    def test_get_own_bids_empty(self):
        bids = ob.get_own_bids()
        assert bids == [], 'Expected {}, got {}'.format([], bids)

    def test_get_own_bids(self):
        bid = ob.create_bid(1, 1, next_year)
        bids = ob.get_own_bids()
        assert bids == [bid], 'Expected {}, got {}'.format([bid], bids)
