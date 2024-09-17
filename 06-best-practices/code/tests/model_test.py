import base64
import json
import model 
def test_base64_decode():
    # Encoded data
    encoded_data = 'ewogICAgICAgICJmbG93ZXIiOiB7CiAgICAgICAgICAgICJmbG93ZXJfaWQiOiAiMDEiLAogICAgICAgICAgICAic2VwYWxfbGVuZ3RoIjogNi40LAogICAgICAgICAgICAic2VwYWxfd2lkdGgiOiAzLjIsCiAgICAgICAgICAgICJwZXRhbF9sZW5ndGgiOiA0LjUsCiAgICAgICAgICAgICJwZXRhbF93aWR0aCI6IDEuNQogICAgICAgICAgICB9LCAKICAgICAgICAiZmxvd2VyX2lkIjogMTU2CiAgICB9'
    
    # Decode the base64 encoded string and load it as a JSON object
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    flower_event = json.loads(decoded_data)
    
    # Extract flower details and ID
    flower_dict = flower_event['flower']
    # flower_id = flower_event['flower_id']
    
    # Define the expected flower data and ID
    expected_flower = {
        "sepal_length": 6.4,
        "sepal_width": 3.2,
        "petal_length": 4.5,
        "petal_width": 1.5
    }
    # expected_id = "01"
    
    # Remove 'flower_id' from the flower_dict to match the expected_flower structure
    flower_data = {key: flower_dict[key] for key in ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']}
    
    # Assert that the extracted data matches the expected data
    assert flower_data == expected_flower, f"Expected {expected_flower}, but got {flower_data}"
    # assert flower_id == expected_id, f"Expected {expected_id}, but got {flower_id}"

def test_predict():
    # Initialize the model with a valid run_id
    model_service = model.init('flower_stream','72e6547ed6a24ee9bebedb981ea11114', '123', False)

    # Input features for prediction
    features = {
        "sepal_length": 6.4,
        "sepal_width": 3.2,
        "petal_length": 4.5,
        "petal_width": 1.5
    }
    
    flower = model.IrisInput(**features)

    actual_prediction = model_service.predict_iris(flower)

    expected_prediction = "versicolor" 

    assert actual_prediction["prediction"] == expected_prediction
def test_lambda_handler():
        event = {
            "Records": [
                {
                    "kinesis": {
                                        "data": "ewogICAgICAgICJmbG93ZXIiOiB7CiAgICAgICAgICAgICJmbG93ZXJfaWQiOiAiMDEiLAogICAgICAgICAgICAic2VwYWxfbGVuZ3RoIjogNi40LAogICAgICAgICAgICAic2VwYWxfd2lkdGgiOiAzLjIsCiAgICAgICAgICAgICJwZXRhbF9sZW5ndGgiOiA0LjUsCiAgICAgICAgICAgICJwZXRhbF93aWR0aCI6IDEuNQogICAgICAgICAgICB9LCAKICAgICAgICAiZmxvd2VyX2lkIjogMTU2CiAgICB9==",
                    },
                }
            ]
        }
        model_service = model.init('flower_stream','72e6547ed6a24ee9bebedb981ea11114', '123', False)
        response = model_service.lambda_handler(event)

        # Expected prediction result
        expected_prediction = {
            'model': 'model_type',
            'version': model_service.model_version,
            'prediction': {
                'flower': {'prediction': 'versicolor'},
                'flower_id': 156
            }
        }
        assert response['predictions'][0] == expected_prediction