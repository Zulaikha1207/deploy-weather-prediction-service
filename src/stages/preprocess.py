import os
import sys
import pandas as pd
from sklearn import preprocessing
from typing import Text
import yaml
import argparse

def count_nulls_by_line(df):
    return df.isnull().sum().sort_values(ascending=False)

def null_percent_by_line(df):
    return (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)

def preprocess(config_path: Text) -> None:
    with open("params.yaml") as config_file:
        config = yaml.safe_load(config_file)
    
    df = pd.read_csv(config['data']['path_data'])
    print('Loading data. Shape of raw data: ', df.shape)

    zeros_cnt = count_nulls_by_line(df)
    percent_zeros = null_percent_by_line(df)
    missing_data = pd.concat([zeros_cnt, percent_zeros], axis=1, keys=["Total", "Percent"])
    dropList = list(missing_data[missing_data["Percent"] > config['data_preprocessing']['drop_percent']].index)
    df.drop(dropList, axis=1, inplace=True)
    df.drop(["Date"], axis=1, inplace=True)
    df.drop(["Location"], axis=1, inplace=True)
    print('Getting rid of features with high percent of missing values. New shape is: ', df.shape)

    print('Performing one hot encoding on categorical features...')
    preprocessed_df = pd.get_dummies(data=df, columns=["WindGustDir", "WindDir9am", "WindDir3pm"])
    preprocessed_df["RainToday"] = df["RainToday"].astype(str)
    preprocessed_df["RainTomorrow"] = df["RainTomorrow"].astype(str)
    lb = preprocessing.LabelBinarizer()
    preprocessed_df["RainToday"] = lb.fit_transform(preprocessed_df["RainToday"])
    preprocessed_df["RainTomorrow"] = lb.fit_transform(preprocessed_df["RainTomorrow"])
    
    cols = preprocessed_df.columns.tolist()
    cols.remove("RainTomorrow")
    cols.append("RainTomorrow")
    preprocessed_df = preprocessed_df[cols]
    preprocessed_df = preprocessed_df.dropna()
    preprocessed_df = preprocessed_df.reset_index()
    preprocessed_df = preprocessed_df.drop(['index'], axis=1)
    print('preprocessed df shape\n', preprocessed_df.shape)
    print('preprocessed df\n', preprocessed_df)
    preprocessed_df.to_csv(config['data_preprocessing']['preprocessed_csv'], index=False)
    
    #features_df = preprocessed_df.drop(["RainTomorrow"], axis=1)
    #print('Features df shape\n', features_df.shape)
    #print('Features df\n', features_df)
    #features_df.to_csv(config['data_preprocessing']['features_csv'], index=False)
    print('Preprocessing is complete!!')

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()


    preprocess(config_path=args.config)
