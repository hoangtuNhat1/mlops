import model 
import os 

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME')
TEST_RUN = os.getenv('TEST_RUN')
RUN_ID = os.getenv('RUN_ID')
model_services = model.init(PREDICTIONS_STREAM_NAME, RUN_ID, RUN_ID,TEST_RUN)

def lambda_handler(event, context):
    return model_services.lambda_handler(event)
