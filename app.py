import streamlit as st
import pandas as pd

# Google Sheets 設定
SHEET_URL = "https://docs.google.com/spreadsheets/d/1AzJ6IJayXV7yooFJyWRhDvD0cDGWTexl_hjjtVF4JGs"
SHEET_NAME_MAP = {
    "category": "商品類別",
    "feature": "特徵",
    "color": "顏色/材質",
    "size": "尺寸"
}

@st.cache_data(show_spinner=False)
def load_dropdown_options():
    sheet_id = SHEET_URL.split("/")[5]
    base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="
    options = {}
    for key, sheet_name in SHEET_NAME_MAP.items():
        url = base_url + sheet_name
        try:
            df = pd.read_csv(url, header=None, encoding='utf-8')
            options[key] = dict(zip(df[0], df[0]))  # 取第一欄作為選單
            st.write(f"✅ 已成功載入「{sheet_name}」，共 {len(df)} 筆")
        except Exception as e:
            error_msg = str(e).encode('utf-8', errors='ignore').decode()
            st.warning(f"⚠️ 無法載入「{sheet_name}」選項，請檢查分享權限或欄位格式。\n錯誤訊息: {error_msg}")
            options[key] = {}
    return options

def generate_sku(category, feature, color, size):
    return f"{category}-{feature}-{color}-{size}"

# UI
st.set_page_config(page_title="Product SKU Generator", layout="centered")
st.title("🧾 Product SKU Generator")

options = load_dropdown_options()

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Product Category", options.get("category", {}).keys())
    size = st.selectbox("Size", options.get("size", {}).keys())
with col2:
    color = st.selectbox("Color", options.get("color", {}).keys())
    feature = st.selectbox("Feature", options.get("feature", {}).keys())

if st.button("➕ Generate SKU"):
    if category and color and size and feature:
        sku = generate_sku(
            options["category"][category],
            options["feature"][feature],
            options["color"][color],
            options["size"][size],
        )
        st.success(f"✅ SKU: `{sku}`")
    else:
        st.warning("請完整選取所有欄位後再產生 SKU。")
else:
    st.info("尚未產生任何 SKU。請從上方輸入資料。")
