from goods.offer import OfferToSell

class Fixed:
    def __init__(self, price_strategy):
        self.price_strategy = price_strategy

    def compute_offers(self, producer_id, inventory):
        offers = []
        for good in inventory.quantity:
            if inventory.quantity[good] > 0:
                offers.append(OfferToSell(producer_id, good, inventory.quantity[good], self.price_strategy.compute_price()))
        return offers
