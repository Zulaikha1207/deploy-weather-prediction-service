import os
import sys
import yaml
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature
from ibm_ai_openscale.supporting_classes.enums import *
import requests
from ibm_ai_openscale.utils import get_instance_guid
import ibm_watson_machine_learning
import json
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson_openscale import *
from ibm_watson_openscale.supporting_classes.enums import *
from ibm_watson_openscale.supporting_classes.payload_record import PayloadRecord
import ibm_watson_openscale


PROJ_PATH = os.path.abspath(sys.argv[1])
CRED_PATH = os.path.abspath(sys.argv[2])
META_PATH = PROJ_PATH + "/metadata.yaml"


with open(CRED_PATH) as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


with open(META_PATH) as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

service_credentials = {
    "apikey": credentials["apikey"],
    "url": "https://api.aiopenscale.cloud.ibm.com",
}

DEPLOYMENT_UID = metadata["deployment_uid"]
MODEL_UID = metadata["model_uid"]
MODEL_NAME = metadata["project_name"] + "_" + metadata["project_version"]
SPACE_ID = credentials["space_id"]
WOS_GUID = get_instance_guid(api_key=service_credentials["apikey"])

WOS_CREDENTIALS = {
    "instance_guid": WOS_GUID,
    "apikey": service_credentials["apikey"],
    "url": "https://api.aiopenscale.cloud.ibm.com"
}

if WOS_GUID is None:
    print("Watson OpenScale GUID NOT FOUND")
else:
    print(WOS_GUID)

wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

wml_client = ibm_watson_machine_learning.APIClient(wml_credentials)

wml_credentials = {
    "url": credentials["url"],
    "apikey": credentials["apikey"],
    "instance_id": "wml_local",
}

wml_client.set.default_space(SPACE_ID)

authenticator = IAMAuthenticator(apikey=credentials["apikey"])
wos_client = ibm_watson_openscale.APIClient(
    authenticator=authenticator, service_url="https://api.aiopenscale.cloud.ibm.com"
)

for deployment in wml_client.deployments.get_details()['resources']:
    if DEPLOYMENT_UID in deployment['metadata']['id']:

        scoring_endpoint = deployment['entity']['status']['online_url']['url']

print(scoring_endpoint)
wos_client.subscriptions.show()

with open("params.yaml") as config_file:
        config = yaml.safe_load(config_file)

df_data = pd.read_csv(config['data_preprocessing']['preprocessed_csv'])

X = df_data.iloc[:, :-1]
y = df_data[df_data.columns[-1]]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.01, random_state=1337
)

payload_scoring = {
    "input_data": [
        {
            "fields": X.columns.to_numpy().tolist(),
            "values": X_test.to_numpy().tolist(),
        }
    ]
}

scoring_response = wml_client.deployments.score(DEPLOYMENT_UID, payload_scoring)
subscription_id = '0b0dea74-1f19-48ae-a04f-6899aaebf9a7'


payload_data_set_id = wos_client.data_sets.list(type=DataSetTypes.PAYLOAD_LOGGING, target_target_id=subscription_id, target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id

print("Payload data set id:", payload_data_set_id)

records = [PayloadRecord(request=payload_scoring, response=scoring_response, response_time=72)]
store_record_info = wos_client.data_sets.store_records(payload_data_set_id, records)