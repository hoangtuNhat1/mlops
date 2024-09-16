from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import uvicorn
# Load the model and DictVectorizer
with open('./models/lin_reg.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

# FastAPI app
app = FastAPI()

# Request body model
class Ride(BaseModel):
    PULocationID: int
    DOLocationID: int
    trip_distance: float

# Function to prepare features
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride.PULocationID, ride.DOLocationID)
    features['trip_distance'] = ride.trip_distance
    return features

# Prediction function
def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]  # Assuming model.predict returns a list/array

# Define a FastAPI endpoint for prediction
@app.post("/predict")
def predict_ride(ride: Ride):
    features = prepare_features(ride)
    prediction = predict(features)
    return {"prediction": prediction}

if __name__ == "__main__":
    # Start the Uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=2000)
# Run the API using: uvicorn filename:app --reload
