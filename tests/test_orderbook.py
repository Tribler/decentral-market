from nose.tools import assert_equal, assert_is, assert_is_none, assert_is_not_none
import unittest


from tsukiji import orderbook as ob
from tsukiji.crypto import get_public_bytestring

import datetime
now = datetime.datetime.now()
next_year = now.replace(year=now.year + 1)
last_year = now.replace(year=now.year - 1)


class OrderBookTest(unittest.TestCase):

    def setUp(self):
        '''Clean the orderbook before every test.'''
        ob.message_id = 0
        ob.offers = []
        ob.trades = []
        self.public_id = get_public_bytestring()

    def test_create_msg(self):
        message = ob.create_msg()
        assert_equal(type(message), dict)
        assert_equal(message['id'], self.public_id)
        assert_equal(message['message-id'], 0)

    def test_create_msg_incrementing_message_id(self):
        m1 = ob.create_msg()
        m2 = ob.create_msg()

        assert_equal(m1['message-id'], 0)
        assert_equal(m2['message-id'], 1)

    def test_create_msg_passing_options(self):
        options = {
            'hello': 'world',
        }

        message = ob.create_msg(options=options)
        assert 'hello' in message
        assert_equal(message['hello'], 'world')

    def test_create_msg_passing_options_overriding_default(self):
        options = {
            'id': 1234,
        }

        message = ob.create_msg(options=options)
        assert 'id' in message
        assert_equal(message['id'], 1234)

    def test_create_ask(self):
        ask = ob.create_ask(1, 1, now)
        assert_equal(ask['type'], 'ask')
        assert_equal(ask['price'], 1)
        assert_equal(ask['quantity'], 1)
        assert_equal(len(ob.offers), 1)

    def test_create_bid(self):
        import datetime
        ask = ob.create_bid(1, 1, datetime.datetime.now())
        assert_equal(ask['type'], 'bid')
        assert_equal(ask['price'], 1)
        assert_equal(ask['quantity'], 1)
        assert_equal(len(ob.offers), 1)

    def test_create_trade(self):
        trade = ob.create_trade('abcd', 1, 1)
        assert_equal(trade['type'], 'trade')
        assert_equal(trade['recipient'], 'abcd')
        assert_equal(trade['quantity'], 1)
        assert_equal(trade['trade-id'], 1)

    def test_create_confirm(self):
        confirm = ob.create_confirm('abcd', 1)
        assert_equal(confirm['type'], 'confirm')
        assert_equal(confirm['recipient'], 'abcd')
        assert_equal(confirm['trade-id'], 1)

    def test_create_cancel(self):
        cancel = ob.create_cancel('abcd', 1)
        assert_equal(cancel['type'], 'cancel')
        assert_equal(cancel['recipient'], 'abcd')
        assert_equal(cancel['trade-id'], 1)

    def test_create_greeting(self):
        greeting = ob.create_greeting()
        assert_equal(greeting['type'], 'greeting')

    def test_create_greeting_response(self):
        greeting_response = ob.create_greeting_response(['abcd', 'efgh'])
        assert_equal(greeting_response['type'], 'greeting_response')
        assert_equal(greeting_response['peerlist'], ['abcd', 'efgh'])

    def test_get_offer(self):
        ask = ob.create_ask(1, 1, next_year)
        offer = ob.get_offer(self.public_id, 0)
        assert_equal(ask, offer)

    def test_get_offer_wrong_message_id(self):
        ob.create_ask(1, 1, next_year)
        offer = ob.get_offer(self.public_id, 1)
        assert_is_none(offer, None)

    def test_get_offer_empty(self):
        offer = ob.get_offer(1, 1)
        assert_is_none(offer, None)

    def test_clean_offers(self):
        ob.create_ask(1, 1, last_year)
        mock_function = lambda *x: x
        ob.clean_offers(mock_function)()
        assert_equal(ob.offers, [])

    def test_trade_offer(self):
        ask = ob.create_ask(1, 2, next_year)
        ask['id'] = 1234
        bid = ob.create_ask(1, 1, next_year)
        trade = ob.trade_offer(ask, bid)
        assert_is_not_none(trade)
        assert_equal(trade['recipient'], 1234)
        assert_equal(trade['quantity'], 1)
        assert_equal(trade['trade-id'], ask['message-id'])

    def test_get_asks_empty(self):
        asks = ob.get_asks()
        assert_equal(asks, [])

    def test_get_asks(self):
        ask = ob.create_ask(1, 1, next_year)
        ask['id'] = 1234
        asks = ob.get_asks()
        assert_equal(asks, [ask])

    def test_get_own_asks_empty(self):
        asks = ob.get_own_asks()
        assert_equal(asks, [])

    def test_get_own_asks(self):
        ask = ob.create_ask(1, 1, next_year)
        asks = ob.get_own_asks()
        assert_equal(asks, [ask])

    def test_get_bids_empty(self):
        bids = ob.get_bids()
        assert_equal(bids, [])

    def test_get_bids(self):
        bid = ob.create_bid(1, 1, next_year)
        bid['id'] = 1234
        bids = ob.get_bids()
        assert_equal(bids, [bid])

    def test_get_own_bids_empty(self):
        bids = ob.get_own_bids()
        assert_equal(bids, [])

    def test_get_own_bids(self):
        bid = ob.create_bid(1, 1, next_year)
        bids = ob.get_own_bids()
        assert_equal(bids, [bid])

    def test_match_bid(self):
        own_bid = ob.create_bid(11, 1, next_year)
        their_ask = ob.create_ask(10, 1, next_year)
        their_ask['id'] = 1234
        matching_ask = ob.match_bid(own_bid)
        assert_is(matching_ask, their_ask)

    def test_match_bid_without_a_match(self):
        own_bid = ob.create_bid(11, 1, next_year)
        their_ask = ob.create_ask(12, 1, next_year)
        their_ask['id'] = 1234
        matching_ask = ob.match_bid(own_bid)
        assert_is_none(matching_ask)

    def test_match_incoming_bid(self):
        own_ask = ob.create_ask(11, 1, next_year)
        their_bid = ob.create_bid(12, 1, next_year)
        their_bid['id'] = 1234
        matching_ask = ob.match_incoming_bid(their_bid)
        assert_is(matching_ask, own_ask)

    def test_match_incoming_bid_without_a_match(self):
        ob.create_ask(12, 1, next_year)
        their_bid = ob.create_bid(11, 1, next_year)
        their_bid['id'] = 1234
        matching_ask = ob.match_incoming_bid(their_bid)
        assert_is_none(matching_ask)

    def test_match_ask(self):
        own_ask = ob.create_ask(11, 1, next_year)
        their_bid = ob.create_bid(12, 1, next_year)
        their_bid['id'] = 1234
        matching_bid = ob.match_ask(own_ask)
        assert_is(matching_bid, their_bid)

    def test_match_ask_without_a_match(self):
        own_ask = ob.create_ask(11, 1, next_year)
        their_bid = ob.create_bid(10, 1, next_year)
        their_bid['id'] = 1234
        matching_bid = ob.match_ask(own_ask)
        assert_is_none(matching_bid)

    def test_match_incoming_ask(self):
        own_bid = ob.create_bid(12, 1, next_year)
        their_ask = ob.create_ask(11, 1, next_year)
        their_ask['id'] = 1234
        matching_bid = ob.match_incoming_ask(their_ask)
        assert_is(matching_bid, own_bid)

    def test_match_incoming_ask_without_a_match(self):
        ob.create_bid(11, 1, next_year)
        their_ask = ob.create_ask(12, 1, next_year)
        their_ask['id'] = 1234
        matching_bid = ob.match_incoming_ask(their_ask)
        assert_is(matching_bid, None)

    def test_lowest_offer_empty(self):
        lowest_offer = ob.lowest_offer([])
        assert_is_none(lowest_offer)

    def test_lowest_offer(self):
        ask = ob.create_ask(1, 1, next_year)
        ob.create_ask(2, 1, next_year)
        lowest_offer = ob.lowest_offer(ob.offers)
        assert_equal(lowest_offer, ask)

    def test_highest_offer_empty(self):
        highest_offer = ob.highest_offer([])
        assert_is_none(highest_offer)

    def test_highest_offer(self):
        ob.create_bid(1, 1, next_year)
        bid2 = ob.create_bid(2, 1, next_year)
        highest_offer = ob.highest_offer(ob.offers)
        assert_equal(highest_offer, bid2)

    def test_remove_offer_empty(self):
        offer = ob.remove_offer(1, 1)
        assert_is_none(offer)

    def test_remove_offer(self):
        ask = ob.create_ask(1, 1, next_year)
        offer = ob.remove_offer(ask['id'], ask['message-id'])
        assert_is(offer, ask)
        assert_equal(ob.offers, [])
