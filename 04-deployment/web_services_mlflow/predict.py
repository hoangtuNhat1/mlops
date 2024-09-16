from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import uvicorn
import mlflow
from sklearn.feature_extraction import DictVectorizer

logged_model = 's3://nir-mlflow-artifacts-bucket/1/72e6547ed6a24ee9bebedb981ea11114/artifacts/models'



app = FastAPI()
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Flower Prediction API!"}

@app.post("/predict")
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


if __name__ == "__main__":
    # Start the Uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=2000)
# Run the API using: uvicorn filename:app --reload
