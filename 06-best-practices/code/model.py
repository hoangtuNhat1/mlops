import base64
import json
import boto3
import os
import mlflow
from pydantic import BaseModel

# Kinesis client initialization
def load_model(run_id: str) :  
        logged_model = f's3://nir-mlflow-artifacts-bucket/1/{run_id}/artifacts/models'
        model = mlflow.pyfunc.load_model(logged_model)
        return model
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class ModelService:
    def __init__(self, model, model_version, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []
    def predict_iris(self, input_data: IrisInput):
        
        """Predict the iris class based on input data."""
        data = [[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]]
        prediction = self.model.predict(data)
        iris_classes = ["setosa", "versicolor", "virginica"]
        predicted_class = iris_classes[prediction[0]]
        return {"prediction": predicted_class}

    def lambda_handler(self, event):
        """Handle incoming Lambda event from Kinesis."""
        predictions = []
        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            flower_event = json.loads(decoded_data)
            flower_dict = flower_event['flower']
            flower_id = flower_event['flower_id']

            # Convert dictionary to IrisInput instance
            flower = IrisInput(**flower_dict)

            # Predict the flower type
            prediction = self.predict_iris(flower)

            # Prepare the prediction event for Kinesis
            predictions_event = {
                'model': 'model_type',
                'version': self.model_version,
                'prediction': {
                    'flower': prediction,
                    'flower_id': flower_id
                }
            }

            # Send the prediction to Kinesis stream if not in test mode
            # if not self.test_run:
            #     kinesis_client.put_record(
            #         StreamName=self.predictions_stream_name,
            #         Data=json.dumps(predictions_event),
            #         PartitionKey=str(flower_id)
            #     )
            for callback in self.callbacks : 
                callback(predictions_event)
            # Collect predictions
            predictions.append(predictions_event)

        # Return all predictions after processing the records
        return {'predictions': predictions}
class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        flower_id = prediction_event['prediction']['flower_id']

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(flower_id),
        )
def init(prediction_stream_name: str, run_id: str, model_version: str, test_run:bool):
        """Initialize the model service with required parameters."""
        model = load_model(run_id)
        callbacks = []
        if not test_run:
                kinesis_client = boto3.client('kinesis')
                kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
                callbacks.append(kinesis_callback.put_record)
        model_service = ModelService(model, model_version)
        return model_service