# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model


# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("best_model_api")

# Create input/output pydantic models   
input_model = create_model("best_model_api_input", **{'age': 60.0, 'sex': 0.0, 'cp': 2.0, 'trestbps': 102.0, 'chol': 318.0, 'fbs': 0.0, 'restecg': 1.0, 'thalach': 160.0, 'exang': 0.0, 'oldpeak': 0.0, 'slope': 2.0, 'ca': 1.0, 'thal': 2.0})
output_model = create_model("best_model_api_output", prediction_label=0, prediction_percentage=0.0, left_percentage=0.0, patients_data={})



# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    
    # Extracting prediction label and prediction score
    prediction_label = predictions["prediction_label"].iloc[0]
    prediction_score = predictions["prediction_score"].iloc[0]

    

    pred_percent = prediction_score * 100
    left_percentage = 100 - pred_percent

    # Round off percentage values to two decimal places
    pred_percent = round(pred_percent, 2)
    left_percentage = round(left_percentage, 2)

     # Remove prediction_label and prediction_score from predictions
    patients_data = predictions.drop(columns=["prediction_label", "prediction_score"]).iloc[0].to_dict()


    
    
    return {"prediction_label": prediction_label, "prediction_percentage": pred_percent, "left_percentage": left_percentage, "patients_data": patients_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
