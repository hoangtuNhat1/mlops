from lambda_function import lambda_handler 
event = {
  "Records": [
    {
      "kinesis": {
        "kinesisSchemaVersion": "1.0",
        "partitionKey": "1",
        "sequenceNumber": "49655790177452839682950274170634725683331377590278553602",
        "data": "ewogICAgICAgICJmbG93ZXIiOiB7CiAgICAgICAgICAgICJmbG93ZXJfaWQiOiAiMDEiLAogICAgICAgICAgICAic2VwYWxfbGVuZ3RoIjogNi40LAogICAgICAgICAgICAic2VwYWxfd2lkdGgiOiAzLjIsCiAgICAgICAgICAgICJwZXRhbF9sZW5ndGgiOiA0LjUsCiAgICAgICAgICAgICJwZXRhbF93aWR0aCI6IDEuNQogICAgICAgICAgICB9LCAKICAgICAgICAiZmxvd2VyX2lkIjogMTU2CiAgICB9==",
        "approximateArrivalTimestamp": 1726211901.682
      },
      "eventSource": "aws:kinesis",
      "eventVersion": "1.0",
      "eventID": "shardId-000000000000:49655790177452839682950274170634725683331377590278553602",
      "eventName": "aws:kinesis:record",
      "invokeIdentityArn": "arn:aws:iam::136165152383:role/lambda-kinesis-role",
      "awsRegion": "ap-southeast-2",
      "eventSourceARN": "arn:aws:kinesis:ap-southeast-2:136165152383:stream/flower_event"
    }
  ]
}
result = lambda_handler(event, None)
print(result)

