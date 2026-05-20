from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load('models/churn_model.pkl')

@app.get("/")
def home():
    return {"message": "RetailBrain AI API Running"}

@app.post('/predict-churn')
def predict_churn(data: dict):

    values = np.array([[
        data['Frequency'],
        data['Monetary'],
        data['AvgOrderValue'],
        data['UniqueProducts'],
        data['PurchaseInterval'],
        data['BasketSize'],
        data['CountryDiversity']
    ]])


    prediction = model.predict(values)[0]

    probability = model.predict_proba(values)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": float(probability)
    }