import os 
import model

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'
RUN_ID = os.getenv('RUN_ID')
model_services = model.init(PREDICTIONS_STREAM_NAME, RUN_ID, RUN_ID,TEST_RUN)
def lambda_handler(event, context):
    # pylint: disable=unused-argument
    return model_services.lambda_handler(event)