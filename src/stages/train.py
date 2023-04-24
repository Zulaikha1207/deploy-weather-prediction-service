import os
import pandas as pd
from typing import Text
import yaml
import argparse
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


def train(config_path: Text) -> None:
    with open("params.yaml") as config_file:
        config = yaml.safe_load(config_file)

    print('Loading processed data...')
    data = pd.read_csv(config['data_preprocessing']['preprocessed_csv'])
    X = data.drop(config['train']['target_column'], axis=1)
    y = data[config['train']['target_column']]

    print('Splitting data into train and test...')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config['train']['test_size'], random_state=config['train']['random_state']
    )

    print('Building Random forest classifier model..')
    pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("RFC", RandomForestClassifier(
                    criterion=config['model']['criterion'],
                    max_depth=config['model']['max_depth'],
                    max_features=config['model']['max_features'],
                    n_estimators=config['model']['n_estimators'],
                ),
            ),
        ]
    )

    training_logs = pipe.fit(X_train, y_train)
    logs = {"training_logs": training_logs}


    print('Saving training pipeline...')
    train_pipe_path= config["train"]["train_pipe_path"]
    #train_metrics_path = config["train"]["train_metrics_path"]
    joblib.dump(pipe, train_pipe_path)
    #joblib.dump(logs, train_metrics_path)
    print('Model training complete!!')
    

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()
    train(config_path=args.config)

