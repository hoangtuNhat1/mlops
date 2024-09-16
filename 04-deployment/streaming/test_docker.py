import base64
import requests
import json
url = "http://localhost:8080/2015-03-31/functions/function/invocations"

# Simulate the input event
flower_data = {
    "flower_id": 1,
    "flower": {
        "sepal_length": 1.5,
        "sepal_width": 0.4,
        "petal_length": 0.5,
        "petal_width": 0.2
    }
}

event = {
    "Records": [
        {
            "kinesis": {
                "data": base64.b64encode(bytes(json.dumps(flower_data), 'utf-8')).decode('utf-8')
            }
        }
    ]
}

# Make the POST request
response = requests.post(url, json=event)
print(response.json())
