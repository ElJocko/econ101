import yaml

def read_config(filepath):
    with open(filepath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
