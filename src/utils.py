from orderbook import get_bids, get_asks, get_own_bids, get_own_asks, trades


def offer_to_string(offer):
    s = "{\n"
    for k, v in offer.iteritems():
        if k == 'id':
            v = v.split('\n')[1][:20] + '...'
        s += "\t{}: {}\n".format(k, v)
    s += "    }"
    return s


def offers_to_string(offers):
    return '\n    '.join(offer_to_string(offer) for offer in offers)


def print_all_offers():

    print '''
    Bids
    =========
    {}

    Asks
    ========
    {}

    Own bids
    ========
    {}

    Own Asks
    ========
    {}

    Trades
    ========
    {}
    '''.format(*[offers_to_string(o) for o in (get_bids(), get_asks(), get_own_bids(), get_own_asks(), trades)])
