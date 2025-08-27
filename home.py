import streamlit as st
import pandas as pd
import urllib
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
            background-color: #000000;
            color: #E8E8E8; /* Slightly brighter grey */
        }

        /* Hero Title Div */
        .title-container {
            background: linear-gradient(90deg, #444444, #000000); /* Brighter grey → Black */
            border-radius: 15px;
            text-align: center;
            box-shadow: 0px 6px 18px rgba(255,255,255,0.1); /* Soft white glow */
            margin-bottom: 20px;
        }

        /* Title Text */
        .title-container h1 {
            font-size: 64px;
            font-weight: 700;
            background: linear-gradient(to right, #F0F0F0, #FFFFFF); /* Soft white → Pure white */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        /* Subtitle */
        .title-container h3 {
            color: #C8C8C8;
            font-weight: 500;
            margin-top: 5px;
        }

        /* Subheaders */
        h2, h3 {
            color: #F0F0F0 !important; /* Brighter grey */
            font-weight: 700;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background-color: #1A1A1A;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #AAAAAA; /* Light grey border */
            box-shadow: 0px 0px 6px rgba(255,255,255,0.05); /* Soft white shadow */
        }

        /* Buttons */
        .stButton button {
            background-color: #CCCCCC;
            color: #000000;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 6px 18px;
        }
        .stButton button:hover {
            background-color: #FFFFFF;
            color: #000000;
        }

        /* Expander (FAQ) */
        .streamlit-expanderHeader {
            background-color: #CCCCCC !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border-radius: 6px;
        }

        /* Contact Us Form */
        .contact-form {
            background-color: #1A1A1A;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #AAAAAA;
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
            border: 1px solid #CCCCCC;
            background-color: #2A2A2A;
            color: #F0F0F0;
        }
        .contact-form button {
            background-color: #CCCCCC;
            color: #000000;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }
        .contact-form button:hover {
            background-color: #FFFFFF;
            color: #000000;
        }

        /* Footer */
        .footer {
            background-color: #1A1A1A;
            color: #CCCCCC;
            text-align: center;
            padding: 15px;
            border-top: 1px solid #AAAAAA;
            margin-top: 50px;
            font-size: 14px;
        }
        .footer a {
            color: #FFFFFF;
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
st.image("assets\hero_image.png")

# ------------------------------
# Quick Stats (dummy placeholders)
# ------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Cars Scraped", "3000+")
with col2:
    st.metric("Brands Covered", "13+")
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
with st.expander("How does Auto Valuer predict prices?"):
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
with st.form("contact_form"):
    name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    query = st.text_area("Your Message", height=150)
    submitted = st.form_submit_button("📨 Create Email")

    if submitted:
        if name and user_email and query:
            subject = urllib.parse.quote("AutoValuer Inquiry / Suggestion")
            body = urllib.parse.quote(f"Name: {name}\nEmail: {user_email}\n\nMessage:\n{query}")
            mailto_link = f"mailto:dakshrana0@gmail.com?subject={subject}&body={body}"

            st.markdown(f"""<a href="{mailto_link}" style="color: inherit; text-decoration: none;">
        👉 Click here to open your email client and send
    </a>
    """,
    unsafe_allow_html=True
)
            st.info("✅ Your message has been pre-filled. Just hit send from your mail app.")
        else:
            st.warning("⚠️ Please complete all fields before submitting.")
# ------------------------------
# Footer Section
# ------------------------------
st.markdown(
    """
    <div class="footer">
        © 2025 AUTO VALUER. All rights reserved. | 
        <a href="https://www.linkedin.com/in/daksh-rana-/" target="_blank">LinkedIn</a> | 
        <a href="https://github.com/dakshhrana0-hub" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
