import streamlit as st
import pandas as pd
import joblib
import datetime

# Load trained model
model = joblib.load("./Data_Cleaning/price_predictor.pkl")

# App config
st.set_page_config(page_title="AUTO VALUER", layout="centered")
st.title("💸 Price Estimator")

st.caption("Estimate used car prices with transparency and confidence.")

# Input section
st.markdown("### 🚘 Enter Car Details")

brand = st.selectbox("Select Brand", ["Maruti", "Hyundai", "Honda", "Toyota", "Ford", "BMW", "Audi"])
year_input = st.text_input("Year of Manufacture (e.g., 2015)", value="2018")
kms_driven = st.number_input("Kilometers Driven", min_value=0, step=1000)

# Validate year input
try:
    year = int(year_input)
    current_year = datetime.datetime.now().year
    if year < 1900 or year > current_year + 1:
        st.error(f"Please enter a valid year between 1900 and {current_year + 1}.")
        st.stop()
except ValueError:
    st.error("Year must be a number.")
    st.stop()

# Predict button
if st.button("Estimate Price"):
    # Prepare input DataFrame
    input_df = pd.DataFrame({
        "Brand": [brand],
        "Year": [year],
        "Kms_Driven": [kms_driven]
    })

    # One-hot encode brand
    input_df = pd.get_dummies(input_df)

    # Align with model features
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_features]

    # Predict
    predicted_price = model.predict(input_df)[0]
    lower = predicted_price * 0.9
    upper = predicted_price * 1.1

    # Display result
    st.subheader("💰 Estimated Price")
    st.success(f"₹{predicted_price:,.0f}")
    st.caption(f"Estimated Range: ₹{lower:,.0f} – ₹{upper:,.0f}")