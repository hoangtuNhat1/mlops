import requests 
ride = {
     'PULocationID': 10, 
     'DOLocationID': 50, 
     'trip_distance': 40
}
url = 'http://127.0.0.1:2000/predict'
response = requests.post(url, json=ride)
print(response.json())
# featues = predict.prepare_featues(ride)
# pred = predict.predict(ride) 
# print(pred)