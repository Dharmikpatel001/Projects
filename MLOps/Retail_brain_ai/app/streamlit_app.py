import streamlit as st
import requests

frequency = st.number_input("Frequency")
monetary = st.number_input("Monetary")
avg_order = st.number_input("AvgOrderValue")
unique_products = st.number_input("UniqueProducts")
purchase_interval = st.number_input("PurchaseInterval")
basket_size = st.number_input("BasketSize")
country_diversity = st.number_input("CountryDiversity")

if st.button("Predict Churn"):

    data = {
        "Frequency": frequency,
        "Monetary": monetary,
        "AvgOrderValue": avg_order,
        "UniqueProducts": unique_products,
        "PurchaseInterval": purchase_interval,
        "BasketSize": basket_size,
        "CountryDiversity": country_diversity
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict-churn",
        json=data
    )

    result = response.json()

    st.success(f"Prediction: {result['churn_prediction']}")
    st.info(f"Churn Probability: {round(result['churn_probability']*100, 2)}%")

    