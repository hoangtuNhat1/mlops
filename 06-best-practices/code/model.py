"""
Module for model loading and Kinesis handling using MLflow and AWS SDK.
Handles the prediction of Iris flower classes and sending predictions to Kinesis streams.
"""

import os
import base64
import json
import boto3
import mlflow
from pydantic import BaseModel

def get_model_path(run_id: str) -> str:
    """Get the path to the model artifact."""
    model_location = os.getenv('MODEL_LOCATION')
    if model_location is not None:
        return model_location
    model_bucket = os.getenv("MODEL_BUCKET", 'nir-mlflow-artifacts-bucket')
    experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID", '1')
    model_path = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/models'
    return model_path

def load_model(run_id: str):
    """Load the MLflow model."""
    model_path = get_model_path(run_id)
    model = mlflow.pyfunc.load_model(model_path)
    return model

def create_kinesis_client():
    """Create a Kinesis client with an optional endpoint URL."""
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')
    if endpoint_url is None:
        return boto3.client('kinesis')
    return boto3.client('kinesis', endpoint_url=endpoint_url)

class IrisInput(BaseModel):
    """Input data schema for Iris flower."""
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class ModelService:
    """Service for model prediction and Kinesis event handling."""
    def __init__(self, model, model_version: str, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def predict_iris(self, input_data: IrisInput) -> dict:
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

            flower = IrisInput(**flower_dict)
            prediction = self.predict_iris(flower)

            predictions_event = {
                'model': 'model_type',
                'version': self.model_version,
                'prediction': {
                    'flower': prediction,
                    'flower_id': flower_id
                }
            }

            for callback in self.callbacks:
                callback(predictions_event)

            predictions.append(predictions_event)

        return {'predictions': predictions}

class KinesisCallback:
    """Callback for sending prediction events to Kinesis."""
    def __init__(self, kinesis_client, prediction_stream_name: str):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event: dict):
        """Send a prediction event to Kinesis."""
        flower_id = prediction_event['prediction']['flower_id']
        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(flower_id),
        )

def init(
prediction_stream_name: str,
run_id: str,
model_version: str,
test_run: bool
) -> ModelService:
    """Initialize the model service with required parameters."""
    model = load_model(run_id)
    callbacks = []
    if not test_run:
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)
    model_service = ModelService(model, model_version, callbacks)
    return model_service
