from agent.producer import Producer
from agent.consumer import Consumer
from goods.type_of_good import TypeOfGood

import random


class Model:
    def __init__(self, number_of_goods, number_of_producers, number_of_consumers, price_0):
        # Create types of goods
        self.goods_list = []
        for i in range(number_of_goods):
            name = 'good_' + str(i)
            type_of_good = TypeOfGood(name)
            self.goods_list.append(type_of_good)

        price_list = {'good_0': price_0, 'good_1': 4, 'good_2': 5}

        # Create producers
        self.producer_list = []
        for i in range(number_of_producers):
            index = random.randrange(number_of_goods)
            type_of_good = self.goods_list[index]
            quantity_per_step = random.randrange(200, 500)
            producer = Producer(self.goods_list, type_of_good, quantity_per_step, price_list[type_of_good.name])
            self.producer_list.append(producer)

        # Create consumers
        self.consumer_list = []
        for i in range(number_of_consumers):
            consumer = Consumer(self.goods_list)
            self.consumer_list.append(consumer)

    def run_trial(self, number_of_steps):
        trial_consumed_goods = {}
        for type_of_good in self.goods_list:
            trial_consumed_goods[type_of_good.name] = 0

        for i in range(number_of_steps):
            # print('Step: {}', i)
            offers_to_sell = []

            # Produce!

            # Loop over the producers
            # Production is order independent
            produced_goods = {}
            for type_of_good in self.goods_list:
                produced_goods[type_of_good.name] = 0

            for producer in self.producer_list:
                producer.produce()
                producer_offers = producer.offer()
                offers_to_sell.extend(producer_offers)
                # print('producer {} produced {} of {} at price {}'.format(producer.id, produced_items.quantity, produced_items.type_of_good.name, produced_items.price))

            # print('produced: {}', produced_goods)

            # Consume!

            # Initialize the tracking dict
            step_consumed_goods = {}
            for type_of_good in self.goods_list:
                step_consumed_goods[type_of_good.name] = 0

            # Choose a random order to select the consumers in
            order_list = []
            for i in range(len(self.consumer_list)):
                order_list.append((i, random.random()))
            order_list.sort(key=lambda item: item[1])

            # Loop over the consumers
            for i in order_list:
                consumer = self.consumer_list[i[0]]
                result = consumer.consume(offers_to_sell)
                if result[0] is not None:
                    step_consumed_goods[result[0]] = step_consumed_goods[result[0]] + result[1]

            # print('consumed this step: {}', step_consumed_goods)

            # Add the results of the step to the trial
            for key in trial_consumed_goods:
                trial_consumed_goods[key] = trial_consumed_goods[key] + step_consumed_goods[key]

        # print('consumed this trial: {}', trial_consumed_goods)

        trial_mean_consumed_goods = {}
        for key in trial_consumed_goods:
            trial_mean_consumed_goods[key] = trial_consumed_goods[key] / number_of_steps
        # print('mean goods consumed: {}'.format(trial_mean_consumed_goods))

        return trial_mean_consumed_goods
