from strategy.producer_production import Fixed as FixedProduction
from strategy.producer_price import Fixed as FixedPrice
from strategy.producer_offer import Fixed as FixedOffer
from goods.inventory import Inventory


class Producer:
    next_id = 0

    def __init__(self, goods_list, type_of_good, quantity_per_step, price):
        self.__assign_id()
        self.inventory = Inventory(goods_list)
        self.type_of_good = type_of_good
        self.price_strategy = FixedPrice(price)
        self.production_strategy = FixedProduction(self.type_of_good, quantity_per_step, self.price_strategy)
        self.offer_strategy = FixedOffer(self.price_strategy)

    def produce(self):
        production = self.production_strategy.produce(self.id)
        self.inventory.quantity[production[0]] += production[1]

    def offer(self):
        offers = self.offer_strategy.compute_offers(self.id, self.inventory)
        return offers

    def __assign_id(self):
        self.id = Producer.next_id
        Producer.next_id += 1
