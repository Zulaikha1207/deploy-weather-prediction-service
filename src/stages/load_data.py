import argparse
import numpy as np
import pandas as pd
import yaml
from typing import Text


def load_data(config_path: Text) -> None:
    with open("params.yaml") as config_file:
        config = yaml.safe_load(config_file)
    
    print('Loading data..')
    dataset = pd.read_csv(config['data']['path_data'])
    print(dataset.head())
    # Save raw data
    dataset.to_csv(config["data"]["path_data"], index=False)
    print('Data load complete!')


#to run from CLI use a constructer that allows to parse config file as an argument to the data_load function
if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    load_data(config_path=args.config)