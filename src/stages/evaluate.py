import os
import pandas as pd
from typing import Text
import yaml
import argparse
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

def evaluate(config_path: Text) -> None:
    with open("params.yaml") as config_file:
        config = yaml.safe_load(config_file)
    
    pipe = joblib.load(config['train']['train_pipe_path'])

    data = pd.read_csv(config['data_preprocessing']['preprocessed_csv'])
    X = data.drop(config['train']['target_column'], axis=1)
    y = data[config['train']['target_column']]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config['train']['test_size'], random_state=config['train']['random_state']
    )

    predictions = pipe.predict(X_test)

   
    accuracy = accuracy_score(y_test, predictions),
    recall = recall_score(y_test, predictions),
    precision = precision_score(y_test, predictions),
    f1 = f1_score(y_test, predictions)

    results = {
        'accuracy': accuracy,
        'recall': recall,
        'precision': precision,
        'f1': f1
    }

    print('Save metrics...')
    # save f1 metrics file
    metrics_path = config['evaluate']['metrics_file_path']

    json.dump(
        obj={'f1_score': results},
        fp=open(metrics_path, 'w')
    )

    print(f'Metrics file saved to : {metrics_path}')

    ##Plot data
    dummy_probs = [0 for _ in range(len(y_test))]
    model_probs = pipe.predict_proba(X_test)
    model_probs = model_probs[:, 1]

    # model_auc = roc_auc_score(y_test, model_probs)

    dummy_fpr, dummy_tpr, _ = roc_curve(y_test, dummy_probs)
    model_fpr, model_tpr, _ = roc_curve(y_test, model_probs)

    # precision_recall_curve
    y_scores = pipe.predict_proba(X_test)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_scores)

    logs = {
        "metrics": results,
        "roc_curve": {
            "model_tpr": model_tpr,
            "model_fpr": model_fpr,
            "dummy_tpr": dummy_tpr,
            "dummy_fpr": dummy_fpr,
        },
        "precision_recall_curve": {
            "precisions": precisions,
            "recalls": recalls,
            "thresholds": thresholds,
        },
    }

    # roc curve
    # plot the roc curve for the model
    plt.plot(
        logs["roc_curve"]["dummy_fpr"],
        logs["roc_curve"]["dummy_tpr"],
        linestyle="--",
        label="Dummy Classifer",
    )
    plt.plot(
        logs["roc_curve"]["model_fpr"],
        logs["roc_curve"]["model_tpr"],
        marker=".",
        label="RFC",
    )
    # axis labels
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    # show the legend
    plt.legend()
    roc_plots_path = config['evaluate']['roc_plots_path']
    plt.savefig(roc_plots_path, dpi=100)
    plt.cla()

    def plot_prc(precisions, recalls, thresholds):
        plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
        plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
        plt.xlabel("Thresholds")
        plt.legend(loc="center left")
        plt.ylim([0, 1])
        precision_recall_plot_path = config['evaluate']['precision_recall_plot_path']
        plt.savefig(precision_recall_plot_path, dpi=100)

    plot_prc(
        logs["precision_recall_curve"]["precisions"],
        logs["precision_recall_curve"]["recalls"],
        logs["precision_recall_curve"]["thresholds"],
    )
    print(f'ROC plot and Precision recall plot saved to: {roc_plots_path}')
    print('Evaluate stage completed!!')



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()
    evaluate(config_path=args.config)