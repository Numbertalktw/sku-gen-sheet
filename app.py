import streamlit as st
import pandas as pd
import requests
import io
import traceback

# Google Sheets 設定
SHEET_URL = "https://docs.google.com/spreadsheets/d/1AzJ6IJayXV7yooFJyWRhDvD0cDGWTexl_hjjtVF4JGs"
SHEET_NAME_MAP = {
    "category": "商品類別",
    "feature": "特徵",
    "color": "顏色/材質",
    "size": "尺寸"
}

# 使用 requests 安全載入 CSV
def fetch_csv_with_requests(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), header=None)

# 快取資料選項
@st.cache_data(show_spinner=False)
def load_dropdown_options():
    sheet_id = SHEET_URL.split("/")[5]
    base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="
    options = {}

    for key, sheet_name in SHEET_NAME_MAP.items():
        url = base_url + sheet_name
        try:
            df = fetch_csv_with_requests(url)
            # 過濾空白列
            df = df[df[0].notna() & (df[0].astype(str).str.strip() != "")]
            options[key] = dict(zip(df[0], df[0]))
            st.write(f"✅ 成功載入「{sheet_name}」，共 {len(df)} 筆")
        except Exception as e:
            error_msg = traceback.format_exc()
            st.warning(f"⚠️ 無法載入「{sheet_name}」，請檢查分享權限或欄位格式。\n\n錯誤訊息:\n{error_msg}")
            options[key] = {}

    return options

# SKU 組合邏輯
def generate_sku(category, feature, color, size):
    return f"{category}-{feature}-{color}-{size}"

# UI 設定
st.set_page_config(page_title="Product SKU Generator", layout="centered")
st.title("🧾 Product SKU Generator")

# 加入手動重新載入選單資料按鈕
if st.button("🔄 重新載入選單資料"):
    st.cache_data.clear()
    st.rerun()

# 載入下拉選單資料
options = load_dropdown_options()

# 排列順序：分類 → 特徵 → 顏色 → 尺寸
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Product Category", options.get("category", {}).keys())
    feature = st.selectbox("Feature", options.get("feature", {}).keys())
with col2:
    color = st.selectbox("Color", options.get("color", {}).keys())
    size = st.selectbox("Size", options.get("size", {}).keys())

# 按鈕產生 SKU
if st.button("➕ Generate SKU"):
    if category and feature and color and size:
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
