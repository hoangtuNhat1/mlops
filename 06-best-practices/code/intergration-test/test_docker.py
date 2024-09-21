import base64
import json

import requests
from deepdiff import DeepDiff

# URL for the Lambda function
url = "http://localhost:2000/2015-03-31/functions/function/invocations"

# Simulate the input event
flower_data = {
    "flower_id": 1,
    "flower": {
        "sepal_length": 1.5,
        "sepal_width": 0.4,
        "petal_length": 0.5,
        "petal_width": 0.2,
    },
}

event = {
    "Records": [
        {
            "kinesis": {
                "data": base64.b64encode(
                    bytes(json.dumps(flower_data), "utf-8")
                ).decode("utf-8")
            }
        }
    ]
}

# Expected response
expected_response = {
    "predictions": [
        {
            "model": "model_type",
            "version": "Test123",
            "prediction": {"flower": {"prediction": "setosa"}, "flower_id": 1},
        }
    ]
}

# Make the POST request
response = requests.post(url, json=event)

# Get the actual response
actual_response = response.json()
print("Actual Response:", json.dumps(actual_response, indent=4))
diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff={diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff


# Use DeepDiff to compare the actual response with the expected response
diff = DeepDiff(
    expected_response, actual_response, ignore_order=True
)  # ignoring order to focus on value differences

# Print the diff result
if diff:
    print("Differences found:", json.dumps(diff, indent=4))
else:
    print("Responses match exactly.")

# Assert that the actual response matches the expected response
assert (
    not diff
), f"Response does not match the expected output. Differences: {json.dumps(diff, indent=4)}"
