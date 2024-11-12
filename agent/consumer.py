import math
import random

class Consumer:
    next_id = 0

    def __init__(self, list_of_goods):
        self.__assign_id()
        self.utils_for_goods = {}
        for good in list_of_goods:
            utils = random.randrange(5)
            self.utils_for_goods[good] = utils

    def consume(self, market):
        money = 200
        max_utils = 0
        max_type = ''
        max_quantity = 0
        for offer in market:
            if offer.quantity > 0:
                available_quantity = min(offer.quantity, math.floor(money / offer.price))
                if available_quantity > 0:
                    offer_utils = available_quantity * self.utils_for_goods[offer.type_of_good]
                    if offer_utils > max_utils:
                        max_utils = offer_utils
                        max_type = offer.type_of_good
                        max_quantity = available_quantity
                        max_offer = offer
        if max_utils > 0:
            # print('consumer {} using {} of {} from producer {}'.format(self.id, max_quantity, max_offer.type_of_good.name, max_offer.producer_id))
            max_offer.quantity -= max_quantity
            return max_type.name, max_quantity
        else:
            return None, 0

    def __assign_id(self):
        self.id = Consumer.next_id
        Consumer.next_id += 1

