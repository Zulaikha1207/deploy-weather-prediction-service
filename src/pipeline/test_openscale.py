import requests
import pandas as pd
import yaml
import os

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = os.environ.get("ibm_cloud_key")
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

with open("params.yaml") as config_file:
    config = yaml.safe_load(config_file)

data = pd.read_csv(config['data_preprocessing']['preprocessed_csv'])
X = data.drop(config['train']['target_column'], axis=1)
#y = data[config['train']['target_column']]

payload_scoring = {
    "input_data": [
        {
            "fields": X.columns.to_numpy().tolist(),
            "values": X[100:105].to_numpy().tolist(),
        }
    ]
}    
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c08b179a-57ff-4375-82aa-5265591ee2d0/predictions?version=2023-02-16', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())