import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Streamlit Page Config
# ------------------------------
st.set_page_config(page_title="AUTO VALUER - Data Insights", page_icon="📊", layout="wide")

# ------------------------------
# Apply Dark Vintage Theme via CSS
# ------------------------------
st.markdown(
    """
    <style>
    /* Overall background & text */
    .stApp {
        background-color: #000000;
        color: #d3d0d0ff;
        font-family: serif;
    }

    /* Hero title container */
    .title-container {
        background: linear-gradient(90deg, #1A1A1A, #000000);
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }
    .title-container h1 {
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(to right, #aba6a6ff, #d3d0d0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .title-container h3 {
        color: #d3d0d0ff;
        font-weight: 500;
        margin-top: 12px;
    }

    /* Highlighted chart headers */
    .chart-header {
        background-color: #1A1A1A;
        padding: 8px 12px;
        border-left: 5px solid #aba6a6ff;
        font-size: 20px;
        font-weight: 700;
        color: #aba6a6ff;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Dataframe */
    .stDataFrame {
        color: #d3d0d0ff;
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 5px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #aba6a6ff;
        color: #000000;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #d3d0d0ff;
        color: #000000;
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
        <h1>📊 Data Insights Dashboard</h1>
        <h3>Explore insights from the scraped OLX Cars Dataset</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Load Dataset
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(".//data/olx_cars_data.csv")

    # Standardize column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    # Ensure proper data types
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Distance_Covered"] = pd.to_numeric(df["Distance_Covered"], errors="coerce")
    df["Brand"] = df["Brand"].str.strip().str.title()

    return df.dropna(subset=["Price", "Year", "Brand"])

df = load_data()

# ------------------------------
# 1. Cars Count per Brand
# ------------------------------
st.markdown('<div class="chart-header">🚗 Cars Count per Brand</div>', unsafe_allow_html=True)
brand_counts = df["Brand"].value_counts()
fig, ax = plt.subplots()
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")
brand_counts.plot(kind="bar", ax=ax, color="#aba6a6ff")
ax.set_xlabel("Brand", color="#d3d0d0ff")
ax.set_ylabel("Car Count", color="#d3d0d0ff")
ax.set_title("", color="#d3d0d0ff")
ax.tick_params(colors="#d3d0d0ff")
st.pyplot(fig)

# ------------------------------
# 2. Average Price per Brand
# ------------------------------
st.markdown('<div class="chart-header">💰 Average Price per Brand</div>', unsafe_allow_html=True)
avg_price = df.groupby("Brand")["Price"].mean().sort_values(ascending=False)
fig, ax = plt.subplots()
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")
avg_price.plot(kind="bar", ax=ax, color="#aba6a6ff")
ax.set_ylabel("Average Price (₹)", color="#d3d0d0ff")
ax.set_title("", color="#d3d0d0ff")
ax.tick_params(colors="#d3d0d0ff")
st.pyplot(fig)

# ------------------------------
# 3. Top 2 Models per Brand
# ------------------------------
st.markdown('<div class="chart-header">🏆 Top 2 Models per Brand</div>', unsafe_allow_html=True)
top_models = df.groupby(["Brand", "Title"]).size().reset_index(name="Count")
top2_per_brand = top_models.groupby("Brand").apply(lambda x: x.nlargest(2, "Count")).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(10, max(4, len(top2_per_brand) * 0.5)))
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")
ax.barh(top2_per_brand["Title"], top2_per_brand["Count"], color="#aba6a6ff")
ax.set_xlabel("Count", color="#d3d0d0ff")
ax.set_ylabel("Car Model", color="#d3d0d0ff")
ax.set_title("", color="#d3d0d0ff")
ax.tick_params(colors="#d3d0d0ff")
st.pyplot(fig)
st.dataframe(top2_per_brand)

# ------------------------------
# 4. Price Distribution by Distance Covered
# ------------------------------
st.markdown('<div class="chart-header">📉 Price Distribution by Distance Covered</div>', unsafe_allow_html=True)
df['Distance_Range'] = pd.cut(df["Distance_Covered"], bins=[0,50000,100000,150000,200000,250000,300000,350000,400000],
                              labels=["0-50k","50k-100k","100k-150k","150k-200k","200k-250k","250k-300k","300k-350k","350k-400k"])
fig, ax = plt.subplots(figsize=(10,5))
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")
df.boxplot(column='Price', by='Distance_Range', ax=ax, patch_artist=True,
           boxprops=dict(facecolor="#aba6a6ff", color="#d3d0d0ff"),
           medianprops=dict(color="#000000"))
ax.set_xlabel("Distance Covered (KM)", color="#d3d0d0ff")
ax.set_ylabel("Price (₹)", color="#d3d0d0ff")
ax.set_title("", color="#d3d0d0ff")
plt.suptitle("")
ax.tick_params(colors="#d3d0d0ff")
st.pyplot(fig)

# ------------------------------
# 5. Price Distribution
# ------------------------------
st.markdown('<div class="chart-header">📦 Price Distribution</div>', unsafe_allow_html=True)
fig, ax = plt.subplots()
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")
ax.hist(df["Price"], bins=10, color="#aba6a6ff", edgecolor="#d3d0d0ff")
ax.set_xlabel("Price (₹)", color="#d3d0d0ff")
ax.set_ylabel("Frequency", color="#d3d0d0ff")
ax.set_title("", color="#d3d0d0ff")
ax.tick_params(colors="#d3d0d0ff")
st.pyplot(fig)

# ------------------------------
# 6. Yearly Price Trend
# ------------------------------
st.markdown('<div class="chart-header">📆 Average Price per Year</div>', unsafe_allow_html=True)
yearly_price = df.groupby("Year")["Price"].mean()
fig, ax = plt.subplots()
fig.patch.set_facecolor("#000000")
ax.set_facecolor("#000000")
yearly_price.plot(kind="line", marker="o", ax=ax, color="#aba6a6ff")
ax.set_xlabel("Year", color="#d3d0d0ff")
ax.set_ylabel("Average Price (₹)", color="#d3d0d0ff")
ax.set_title("", color="#d3d0d0ff")
ax.tick_params(colors="#d3d0d0ff")
st.pyplot(fig)
