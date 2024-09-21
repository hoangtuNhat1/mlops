import json

import boto3

kinesis_client = boto3.client("kinesis", endpoint_url="http://localhost:4566")
stream_name = "flower_predictions"

# Sample data
data = {
    "predictions": [
        {
            "model": "model_type",
            "version": "Test123456",
            "prediction": {"flower": {"prediction": "setosa"}, "flower_id": 1},
        }
    ]
}

response = kinesis_client.put_record(
    StreamName=stream_name, Data=json.dumps(data), PartitionKey="partition_key_1"
)

print(f"Record put response: {response}")
