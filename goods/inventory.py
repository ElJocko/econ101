

class Inventory:
    def __init__(self, goods_list):
        # Initialize the inventory at 0 for each type of good
        self.quantity = {}
        for good in goods_list:
            self.quantity[good] = 0
