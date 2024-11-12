class Fixed:
    def __init__(self, type_of_good, qty_per_step, price_strategy):
        self.type_of_good = type_of_good
        self.qty_per_step = qty_per_step
        self.price_strategy = price_strategy

    def produce(self, producer_id):
        return self.type_of_good, self.qty_per_step
