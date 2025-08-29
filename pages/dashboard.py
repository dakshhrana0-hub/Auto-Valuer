import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    .stApp {
        background-color: #000000;
        color: #d3d0d0;
        font-family: serif;
    }
    .title-container {
        background-color: #1A1A1A;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .title-container h1 {
        font-size: 36px;
        font-weight: 700;
        color: #d3d0d0;
        margin: 0;
    }
    .title-container h1 .emoji {
        font-size: 36px;
        color: inherit;
    }
    .title-container h3 {
        font-size: 18px;
        font-weight: 400;
        color: #aba6a6;
        margin-top: 10px;
    }
    .chart-header {
        background-color: #1A1A1A;
        padding: 6px 10px;
        border-left: 4px solid #aba6a6;
        font-size: 18px;
        font-weight: 600;
        color: #aba6a6;
        border-radius: 4px;
        margin-top: 16px;
        margin-bottom: 8px;
    }
    .stButton>button {
        background-color: #aba6a6;
        color: #000000;
        border-radius: 5px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #d3d0d0;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Hero Title Section
# ------------------------------
st.markdown(
    """
    <div class="title-container">
        <h1><span class="emoji">📊</span> Data Insights Dashboard</h1>
        <h3>Explore insights from the scraped OLX Cars Dataset</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Global Plot Styling
# ------------------------------

# ------------------------------
# Load Dataset
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(".//data/olx_cars_data.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
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

# Count listings per brand
brand_counts = df["Brand"].value_counts()

# Apply Set1 palette from seaborn
colors = sns.color_palette("Set2", n_colors=len(brand_counts))

# Plot
fig, ax = plt.subplots(figsize=(20, 8))
brand_counts.plot(kind="bar", ax=ax, color=colors, edgecolor="#d3d0d0ff")

# Styling
ax.set_title("Number of Listings by Brand", fontsize=18, color="#d3d0d0ff")
ax.set_facecolor("#1A1A1A")
fig.patch.set_facecolor("#1A1A1A")
ax.tick_params(colors="#f1e9e9ff", labelsize=12)
ax.spines['bottom'].set_color('#d3d0d0ff')
ax.spines['left'].set_color('#d3d0d0ff')

st.pyplot(fig)
# ------------------------------
# 2. Average Price per Brand
# ------------------------------

st.markdown('<div class="chart-header">💰 Average Price per Brand</div>', unsafe_allow_html=True)

# Compute average price per brand (in lakhs)
avg_price = df.groupby("Brand")["Price"].mean() / 100000  # Convert to ₹ Lakhs

# Use Seaborn's muted palette
colors = sns.color_palette("muted", n_colors=len(avg_price))

# Plot
fig, ax = plt.subplots(figsize=(20, 8))
avg_price.plot(kind="bar", ax=ax, color=colors, edgecolor="#d3d0d0ff")

# Styling
ax.set_title("Average Price by Brand", fontsize=18, color="#d3d0d0ff", pad=20)
ax.set_ylabel("Average Price (₹ Lakhs)", fontsize=14, color="#d3d0d0ff")
ax.set_facecolor("#1A1A1A")
fig.patch.set_facecolor("#1A1A1A")
ax.tick_params(colors="#d3d0d0ff", labelsize=12)
ax.spines['bottom'].set_color('#d3d0d0ff')
ax.spines['left'].set_color('#d3d0d0ff')
ax.grid(axis='y', linestyle='--', alpha=0.2)

st.pyplot(fig)
# ------------------------------
# 3. Top 2 Models per Brand (Hue by Brand)
# ------------------------------
st.markdown('<div class="chart-header">🏆 Top 2 Models per Brand (Colored by Brand)</div>', unsafe_allow_html=True)
top_models = df.groupby(["Brand", "Title"]).size().reset_index(name="Count")
top2_per_brand = top_models.groupby("Brand").apply(lambda x: x.nlargest(2, "Count")).reset_index(drop=True)
palette = sns.color_palette("husl", len(top2_per_brand["Brand"].unique()))
brand_color_map = dict(zip(top2_per_brand["Brand"].unique(), palette))
colors = top2_per_brand["Brand"].map(brand_color_map)
fig, ax = plt.subplots(figsize=(12, max(4, len(top2_per_brand) * 0.5)))
ax.barh(top2_per_brand["Title"], top2_per_brand["Count"], color=colors)
ax.set_title("Top 2 Models per Brand")
st.pyplot(fig)
st.dataframe(top2_per_brand)

import matplotlib.pyplot as plt
import seaborn as sns

st.markdown('<div class="chart-header">📆 Number of Cars Listed per Year</div>', unsafe_allow_html=True)

# Count listings per year
year_counts = df["Year"].value_counts().sort_index()

# Use a soft palette
colors = sns.color_palette("muted", n_colors=len(year_counts))

# Plot
fig, ax = plt.subplots(figsize=(16, 6))
year_counts.plot(kind="bar", ax=ax, color=colors, edgecolor="#d3d0d0ff")

# Styling
ax.set_title("Number of Listings by Year", fontsize=18, color="#d3d0d0ff", pad=20)
ax.set_xlabel("Year", fontsize=14, color="#d3d0d0ff")
ax.set_ylabel("Number of Cars", fontsize=14, color="#d3d0d0ff")
ax.set_facecolor("#1A1A1A")
fig.patch.set_facecolor("#1A1A1A")
ax.tick_params(colors="#d3d0d0ff", labelsize=12)
ax.spines['bottom'].set_color('#d3d0d0ff')
ax.spines['left'].set_color('#d3d0d0ff')
ax.grid(axis='y', linestyle='--', alpha=0.2)

st.pyplot(fig)

# ------------------------------
# 7. Price vs. Year (Colored by Brand)
# ------------------------------
st.markdown('<div class="chart-header">📍 Price vs. Year (Colored by Brand)</div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(12, 6))
for brand in df["Brand"].unique():
    subset = df[df["Brand"] == brand]
    ax.scatter(subset["Year"], subset["Price"], label=brand, alpha=0.6, s=60)
ax.set_title("Price vs. Year by Brand")
ax.legend(loc="upper right", fontsize="small", frameon=False)
st.pyplot(fig)
