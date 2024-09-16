import requests

# Define the API endpoint
url = "http://127.0.0.1:8000/predict"

# Define the input data to send in the POST request
data = {
    "sepal_length": 6.4,
    "sepal_width": 3.2,
    "petal_length": 4.5,
    "petal_width": 1.5
}

# Send POST request to the API
response = requests.post(url, json=data)

# Print the response from the API
if response.status_code == 200:
    print("Prediction:", response.json())
else:
    print("Error:", response.status_code)
