import requests

url = 'https://localhost:6789/api/runs'
headers = {
    'Authorization': 'Bearer 0b8c8905f1744de091f177dba1ff52e0',
    'Content-Type': 'application/json',
    'Cookie': 'lng=en'
}

data = {
    "run": {
        "pipeline_uuid": "predict",
        "block_uuid": "inference",
        "variables": {
            "inputs": [
                {
                    "DOLocationID": "239",
                    "PULocationID": "236",
                    "trip_distance": 1.98
                }
            ]
        }
    }
}

response = requests.post(url, headers=headers, json=data, verify=False)  # Set verify=False to skip SSL verification
print(response.json())
