import json

from model.standard_model import Model
from config.config import read_config
import pika

def main():
    config = read_config('config/data/config1.yml')

    number_of_experiments = 10
    number_of_trials = 30
    number_of_steps = config['model']['steps']

    print('number of experiments: {}'.format(number_of_experiments))
    print('number of trials per experiment: {}'.format(number_of_trials))
    print('number of steps per trial: {}\n'.format(number_of_steps))

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    except:
        connection = None
        channel = None
        print('Unable to connect to RabbitMQ server, continuing without publishing results\n')

    if connection is not None:
        channel = connection.channel()
        channel.queue_declare(queue='hello')

    for i in range(number_of_experiments):
        price_0 = (i * 1) + 3
        print('Experiment: {}'.format(i))
        print('  price = {}'.format(i, price_0))

        experiment_consumed_goods = []

        # Run the trials
        for j in range(number_of_trials):
            # print('Trial: {}'.format(j))
            # Create the model
            model = Model(config['goods']['number'], config['producers']['number'], config['consumers']['number'], price_0)

            # Run the trial
            trial_consumed_goods = model.run_trial(number_of_steps)

            # Save the results of the trial
            experiment_consumed_goods.append(trial_consumed_goods)

        # Compute experiment results
        experiment_total_consumed_goods = { key.name: 0.0 for key in model.goods_list }
        for trial in experiment_consumed_goods:
            for good in trial:
                experiment_total_consumed_goods[good] = experiment_total_consumed_goods[good] + trial[good]

        experiment_mean_consumed_goods = {k: (v / number_of_trials) for k, v in experiment_total_consumed_goods.items()}
        print('  mean goods consumed: {}'.format(experiment_mean_consumed_goods.values()))

        if channel is not None:
            channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(list(experiment_mean_consumed_goods.values())))

    if connection is not None:
        connection.close()

if __name__ == '__main__':
    main()

