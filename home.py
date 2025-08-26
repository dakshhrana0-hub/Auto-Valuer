import streamlit as st
import pandas as pd

# ------------------------------
# App Config
# ------------------------------
st.set_page_config(
    page_title="AUTO VALUER",
    page_icon="🏎️",
    layout="wide"
)

# ------------------------------
# Custom Black + Purple Theme
# ------------------------------
st.markdown(
    """
    <style>
        /* Overall background */
        .stApp {
            background-color: #000000; /* Black */
            color: #FFFFFF; /* White text */
        }

        /* Hero Image */
        .hero-image {
            width: 100%;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.5);
        }

        /* Hero Title Div */
        .title-container {
            background: linear-gradient(90deg, #6a0dad, #000000); /* Purple → Black */
            padding: 35px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }

        /* Title Text */
        .title-container h1 {
            font-size: 64px;
            font-weight: 900;
            background: linear-gradient(to right, #9b59b6, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        /* Subtitle */
        .title-container h3 {
            color: #dcdcdc;
            font-weight: 500;
            margin-top: 12px;
        }

        /* Subheaders */
        h2, h3 {
            color: #BA55D3 !important;
            font-weight: 700;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background-color: #1A1A1A;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #9B30FF;
        }

        /* Buttons */
        .stButton button {
            background-color: #9B30FF;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 6px 18px;
        }
        .stButton button:hover {
            background-color: #BA55D3;
            color: black;
        }

        /* Expander (FAQ) */
        .streamlit-expanderHeader {
            background-color: #9B30FF !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 6px;
        }

        /* Contact Us Form */
        .contact-form {
            background-color: #1A1A1A;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #9B30FF;
        }
        .contact-form label {
            font-weight: 600;
            margin-top: 10px;
        }
        .contact-form input, .contact-form textarea {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid #BA55D3;
            background-color: #2A2A2A;
            color: white;
        }
        .contact-form button {
            background-color: #9B30FF;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }
        .contact-form button:hover {
            background-color: #BA55D3;
            color: black;
        }

        /* Footer */
        .footer {
            background-color: #1A1A1A;
            color: #BA55D3;
            text-align: center;
            padding: 15px;
            border-top: 1px solid #9B30FF;
            margin-top: 50px;
            font-size: 14px;
        }
        .footer a {
            color: #BA55D3;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Hero Title Section with DIV
# ------------------------------
st.markdown(
    """
    <div class="title-container">
        <h1>AUTO VALUER</h1>
        <h3>Extract • Analyze • Compare • Decide</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Hero Image Section (Below Title)
# ------------------------------
st.markdown(
    """
    <img class="hero-image" src="./assets/1234.jpg" alt="Hero Image">
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Quick Stats (dummy placeholders)
# ------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Cars Scraped", "4,280+")
with col2:
    st.metric("Brands Covered", "35+")
with col3:
    st.metric("Avg Price Range", "₹1.5L – ₹12L")

# ------------------------------
# Navigation Cards
# ------------------------------
st.markdown("### 🔍 Explore the Modules")
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📊 Car Inventory Dashboard")
    st.write("Browse all scraped cars with filters, search, and trend charts.")
    if st.button("Go to Dashboard ➡️"):
        st.switch_page("pages/1_Dashboard.py")

    st.markdown("#### 🤖 GenAI Decision Assistant")
    st.write("Ask natural language questions and get smart recommendations.")
    if st.button("Chat with Assistant ➡️"):
        st.switch_page("pages/2_Assistant.py")

with col2:
    st.markdown("#### 💰 Price Prediction")
    st.write("Estimate a car’s fair value using our regression model.")
    if st.button("Predict Price ➡️"):
        st.switch_page("pages/3_PricePrediction.py")

    st.markdown("#### ⚖️ Car Comparison")
    st.write("Compare two cars side-by-side with key insights.")
    if st.button("Compare Cars ➡️"):
        st.switch_page("pages/4_Comparison.py")

# ------------------------------
# FAQ Section
# ------------------------------
st.markdown("---")
st.header("❓ Frequently Asked Questions")
with st.expander("How does Car Compare AI predict prices?"):
    st.write("We use a **Multiple Linear Regression model** trained on scraped data to estimate fair car values.")
with st.expander("Which platforms do you scrape data from?"):
    st.write("Currently from **OLX** and **CarsDekho24**, with plans to expand to Cars24 and Spinny.")
with st.expander("Can I trust the AI recommendations?"):
    st.write("Our GenAI assistant combines regression output, brand history, and depreciation trends to give **context-aware suggestions** — but final decisions should always involve inspection and negotiation.")
with st.expander("Do you store my personal data?"):
    st.write("No personal user data is stored. We only process public car listing data for analysis.")

# ------------------------------
# Contact Us Form Section
# ------------------------------
st.markdown("---")
st.header("📩 Contact Us")

# Form fields
name = st.text_input("Your Name")
email = st.text_input("Your Email")
message = st.text_area("Your Message")

if st.button("✉️ Create Email"):
    st.success(f"Thanks {name}! Your message has been prepared for sending.")
    st.info(f"Email: {email}\nMessage: {message}")

# ------------------------------
# Footer Section
# ------------------------------
st.markdown(
    """
    <div class="footer">
        © 2025 AUTO VALUER. All rights reserved. | 
        <a href="https://www.linkedin.com" target="_blank">LinkedIn</a> | 
        <a href="https://github.com" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
