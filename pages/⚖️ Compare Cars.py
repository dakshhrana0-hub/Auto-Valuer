import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# ------------------------------
# Setup
# ------------------------------
load_dotenv()
API_KEY = os.getenv(".GROQ_API_KEY")

st.set_page_config(page_title="AUTO VALUER", layout="wide")
st.markdown("### ⚖️ Compare Two Cars")
st.write("Select two cars to compare their specifications and get a smart recommendation.")

# ------------------------------
# Load and format data
# ------------------------------
mydata = pd.read_csv("Data/olx_cars_data.csv")  # Adjust path if needed

def format_label(row):
    return f"{row['Title']} | ₹{round(row['Price']/100000,2)}L | {row['Distance Covered']} KM | {row['Location']}"

mydata["Label"] = mydata.apply(format_label, axis=1)

# ------------------------------
# Car Selection with Placeholder
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    car1_label = st.selectbox(
        "Select Car 1",
        options=mydata["Label"],
        index=None,
        placeholder="Type or select a car model"
    )

with col2:
    car2_label = st.selectbox(
        "Select Car 2",
        options=mydata["Label"],
        index=None,
        placeholder="Type or select a car model"
    )
# ------------------------------
# Comparison Logic (on Submit)
# ------------------------------
if car1_label and car2_label:
    if st.button("Compare Cars 🚀"):
        if car1_label == car2_label:
            st.warning("Sorry ! You can't compare same car. Please try any other comparison ...")
        else:
            car1 = mydata[mydata["Label"] == car1_label].iloc[0]
            car2 = mydata[mydata["Label"] == car2_label].iloc[0]

            st.markdown("#### 🔍 Side-by-Side Comparison")

            # Inject custom CSS for link styling
            st.markdown("""
            <style>
                a.custom-link {
                    text-decoration: none !important;
                    color: #F5F5F5;
                    font-weight: 600;
                    transition: background-color 0.3s ease;
                }
                a.custom-link:hover {
                    color: #708090 !important;
                }
            </style>
            """, unsafe_allow_html=True)

            def display_comparison(c1, c2):
                st.markdown(f"""
                <table style="width:100%; font-size:16px; border-collapse:collapse;">
                    <thead>
                        <tr style="background-color:#1A1A1A;">
                            <th style="text-align:left; padding:8px;">Attribute</th>
                            <th style="text-align:left; padding:8px;">{c1['Title']}</th>
                            <th style="text-align:left; padding:8px;">{c2['Title']}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Brand</td><td>{c1['Brand']}</td><td>{c2['Brand']}</td></tr>
                        <tr><td>Year</td><td>{c1['Year']}</td><td>{c2['Year']}</td></tr>
                        <tr><td>Price (₹)</td><td>{round(c1['Price']/100000,2)}L</td><td>{round(c2['Price']/100000,2)}L</td></tr>
                        <tr><td>Distance Covered (KM)</td><td>{c1['Distance Covered']}</td><td>{c2['Distance Covered']}</td></tr>
                        <tr><td>Location</td><td>{c1['Location']}</td><td>{c2['Location']}</td></tr>
                        <tr><td>Link</td>
                            <td><a class="custom-link" href="{c1['Link']}" target="_blank">Visit Listing 🔗</a></td>
                            <td><a class="custom-link" href="{c2['Link']}" target="_blank">Visit Listing 🔗</a></td>
                        </tr>
                    </tbody>
                </table>
                """, unsafe_allow_html=True)

            display_comparison(car1, car2)

        # ------------------------------
        # Smart Suggestion
        # ------------------------------
        if car1_label != car2_label:
            st.markdown("#### 🤖 Smart Recommendation")

        def query_groq_model(c1, c2):
            llm = ChatGroq(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0,
                max_retries=2,
                groq_api_key=API_KEY
            )

            prompt = f"""
You are an assistant helping users compare two used cars. Be honest, helpful, and concise.

Car 1:
Title: {c1['Title']}
Brand: {c1['Brand']}
Year: {c1['Year']}
Price: ₹{c1['Price']}
Distance Covered: {c1['Distance Covered']} KM
Location: {c1['Location']}

Car 2:
Title: {c2['Title']}
Brand: {c2['Brand']}
Year: {c2['Year']}
Price: ₹{c2['Price']}
Distance Covered: {c2['Distance Covered']} KM
Location: {c2['Location']}

Which car offers better value and why? 
You have to give a final decison to choose a car.
"""

            try:
                response = llm.invoke(prompt)
                return response.content.strip()
            except Exception:
                return generate_fallback_suggestion(c1, c2)

        def generate_fallback_suggestion(c1, c2):
            price_diff = c2["Price"] - c1["Price"]
            year_diff = c2["Year"] - c1["Year"]
            km_diff = c2["Distance Covered"] - c1["Distance Covered"]

            if price_diff > 0 and km_diff > 0:
                return f"💡 **{c1['Title']}** may offer better value with lower price and mileage."
            elif year_diff > 0 and price_diff < 0:
                return f"✅ **{c2['Title']}** is newer and cheaper — a strong pick."
            else:
                return f"🤔 Both cars have trade-offs. Prefer lower mileage? Go with **{c1['Title']}**. Want a newer model? Consider **{c2['Title']}**."

        if car1_label != car2_label:
            suggestion = query_groq_model(car1, car2)
            st.markdown(suggestion)