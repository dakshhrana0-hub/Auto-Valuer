import streamlit as st
import pandas as pd

# Load your data
df = pd.read_csv('./Data/olx_cars_data.csv')

# Page config
st.set_page_config(page_title="Car Listings Explorer", layout="wide")
st.title("🚗 OLX Car Listings Explorer")

# --- Filters ---
col1, col2 = st.columns(2)

# Capitalize brand names for display only
unique_brands = sorted(df['Brand'].dropna().unique())
display_brands = [b.capitalize() for b in unique_brands]

with col1:
    selected_brand_display = st.selectbox("Choose Brand", options=display_brands)
    selected_brand = selected_brand_display.lower()  # for filtering

with col2:
    selected_year = st.slider(
        "Select Year Range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(int(df["Year"].min()), int(df["Year"].max()))
    )

# Optional model name search
search_term = st.text_input("🔍 Search by Model Name", value="", help="Type part of the car title (e.g. 'Swift', 'Creta')")

submit = st.button("🚀 Show Listings")

# --- Display Section ---
if submit:
    # Title filter: optional
    title_filter = df["Title"].str.lower().str.contains(search_term.lower()) if search_term.strip() else pd.Series([True] * len(df))

    # Apply all filters
    filtered_df = df[
        (df["Brand"].str.lower() == selected_brand) &
        (df["Year"] >= selected_year[0]) &
        (df["Year"] <= selected_year[1]) &
        title_filter
    ]

    st.markdown(f"### 🔍 Showing {len(filtered_df)} listings for **{selected_brand_display}** ({selected_year[0]}–{selected_year[1]})")

    for _, row in filtered_df.iterrows():
        has_image = pd.notna(row["Image"]) and str(row["Image"]).strip() != ""

        # --- Content Block ---
        content_block = f"""
        <h3 style='color:#d3d0d0ff; margin-bottom:8px; font-family:Georgia, serif;'>{row['Title']}</h3>
        <p style='color:#aba6a6ff; font-size:15px; margin:0; font-family:Georgia, serif;'>
            📍 <strong>Location:</strong> {row['Location']} &nbsp; 📅 <strong>Year:</strong> {row['Year']}<br>
            🚗 <strong>Distance Covered:</strong> {row['Distance Covered']} <br>💰 <strong>Price:</strong> ₹{round(row['Price']/100000,2)}L
        </p>
        <a href="{row['Link']}" target="_blank">
            <button style="
                margin-top:12px;
                background-color:#767474ff;
                color:#000000;
                padding:8px 14px;
                border:none;
                border-radius:6px;
                font-weight:bold;
                cursor:pointer;
                font-family:Georgia, serif;
            ">
                🔗 Visit Site
            </button>
        </a>
        """

        # --- Layout with optional image ---
        if has_image:
            img_tag = f"<img src='{row['Image']}' style='width:180px; height:auto; border-radius:8px; border:1px solid #444;' />"
            inner_layout = f"<div style='display:flex; gap:20px; align-items:center;'>{img_tag}<div style='flex:1;'>{content_block}</div></div>"
        else:
            inner_layout = f"<div>{content_block}</div>"

        # --- Card Container ---
        st.markdown(f"""
        <div style='
            background-color:#1A1A1A;
            padding:20px;
            margin-bottom:20px;
            border-radius:12px;
            box-shadow:0 0 12px rgba(255,255,255,0.05);
            border:1px solid #2A2A2A;
            font-family:Georgia, serif;
        '>
            {inner_layout}
        </div>
        """, unsafe_allow_html=True)