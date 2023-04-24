import requests

ride = {
    "PULocationID": 66,
    "DOLocationID": 32,
    "trip_distance": 100
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=ride)
print(response.json())
