
bids = []
offers = []


def match_bid(bid):
    offer = lowest_offer()
    return offer if offer['price'] <= bid['price'] else None


def lowest_offer(offers=offers):
    return min(offers, key=lambda x: x['price'])
