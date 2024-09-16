import base64
import json
import boto3
import os
import mlflow
from pydantic import BaseModel
kinesis_client = boto3.client('kinesis')
PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'flower_predictions')
TEST_RUN = os.getenv('TEST_RUN', True)
logged_model = 's3://nir-mlflow-artifacts-bucket/1/72e6547ed6a24ee9bebedb981ea11114/artifacts/models'
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
def predict_iris(input_data: IrisInput):
    model = mlflow.pyfunc.load_model(logged_model)
    data = [[
        input_data.sepal_length,
        input_data.sepal_width,
        input_data.petal_length,
        input_data.petal_width
    ]]
    prediction = model.predict(data)
    iris_classes = ["setosa", "versicolor", "virginica"]
    predicted_class = iris_classes[prediction[0]]
    return {"prediction": predicted_class}
def lambda_handler(event, context):
    predictions = []
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        flower_event = json.loads(decoded_data)
        flower_dict = flower_event['flower']
        flower_id = flower_event['flower_id']
        # Convert dictionary to IrisInput instance
        flower = IrisInput(**flower_dict)
        prediction = predict_iris(flower)
        predictions_event = {
            'model': 'model_type',
            'model_version': '123',
            'prediction': {
                'flower': prediction,
                'flower_id': flower_id
            }
        }
        if not TEST_RUN: 
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(predictions_event),
                PartitionKey=str(flower_id)
            )
        predictions.append(predictions_event)
    return {'predictions': predictions}
