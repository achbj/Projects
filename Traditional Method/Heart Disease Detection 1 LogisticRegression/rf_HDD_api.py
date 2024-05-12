# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("rf_HDD_api")

# Create input/output pydantic models
input_model = create_model("rf_HDD_api_input", **{'age': 53.0, 'sex': 1.0, 'cp': 2.0, 'trestbps': 130.0, 'chol': 246.0, 'fbs': 1.0, 'restecg': 0.0, 'thalach': 173.0, 'exang': 0.0, 'oldpeak': 0.0, 'slope': 2.0, 'ca': 3.0, 'thal': 2.0})
output_model = create_model("rf_HDD_api_output", prediction=0)


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
