import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 連線設定
SHEET_URL = "https://docs.google.com/spreadsheets/d/1AzJ6IJayXV7yooFJyWRhDvD0cDGWTexl_hjjtVF4JGs"
SHEET_NAME_MAP = {
    "category": "商品類別",
    "color": "顏色",
    "size": "尺寸",
    "material": "材質"
}

@st.cache_data(show_spinner=False)
def load_dropdown_options():
    sheet_id = SHEET_URL.split("/")[5]
    base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

    options = {}
    for key, sheet_name in SHEET_NAME_MAP.items():
        url = base_url + sheet_name
        try:
            df = pd.read_csv(url)
            options[key] = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        except Exception as e:
            options[key] = {}
    return options

def generate_sku(category, color, size, material):
    return f"{category[:2]}-{color[:2]}-{size[:1]}-{material[:2]}".upper()

# App 介面
st.set_page_config(page_title="Product SKU Generator", layout="centered")
st.title("🧾 Product SKU Generator")

options = load_dropdown_options()

col1, col2 = st.columns(2)
with col1:
    selected_category = st.selectbox("Product Category", list(options["category"].keys()))
    selected_size = st.selectbox("Size", list(options["size"].keys()))
with col2:
    selected_color = st.selectbox("Color", list(options["color"].keys()))
    selected_material = st.selectbox("Material", list(options["material"].keys()))

if st.button("➕ Generate SKU"):
    sku = generate_sku(
        options["category"][selected_category],
        options["color"][selected_color],
        options["size"][selected_size],
        options["material"][selected_material]
    )
    st.success(f"產生的 SKU：`{sku}`")
else:
    st.info("尚未產生任何 SKU。請從上方輸入資料。")
