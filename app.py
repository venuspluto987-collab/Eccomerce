import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="E-Commerce Dashboard")

# 🌈 COLORFUL BACKGROUND
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ff4b5c, #ff758c, #5f2c82, #00c6ff);
    background-attachment: fixed;
}

[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.15);
    padding: 15px;
    border-radius: 15px;
    color: white;
}

.stDataFrame {
    background-color: rgba(255,255,255,0.15);
    border-radius: 12px;
}

.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.2);
    color: white;
}

h1, h2, h3 {
    color: white !important;
}

.block-container {
    padding-top: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# Load Data
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")

# Title
st.markdown("<h2 style='text-align:center;'>🛒 E-Commerce AI Chatbot Dashboard</h2>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

# Products Table
with col1:
    st.subheader("📦 Products Table")
    st.dataframe(products, use_container_width=True, height=250)

# Stock Chart
with col2:
    st.subheader("📊 Stock Chart")
    st.bar_chart(products.set_index("product")["stock"], height=250)

# Bottom Layout
col3, col4 = st.columns(2)

# Chatbot
with col3:
    st.subheader("🤖 Chatbot")
    user_input = st.text_input("Ask product price or order tracking")

    reply = "Ask me product price or order tracking 😊"

    if user_input:
        user_input = user_input.lower()

        for p in products["product"]:
            if p.lower() in user_input and "price" in user_input:
                price = products.loc[products["product"] == p, "price"].values[0]
                reply = f"{p} price is ₹{price}"

        if "track" in user_input or "order" in user_input:
            for oid in orders["order_id"].astype(str):
                if oid in user_input:
                    status = orders.loc[orders["order_id"] == int(oid), "status"].values[0]
                    reply = f"Order {oid} status: {status}"

    st.success(reply)

# Summary
with col4:
    st.subheader("📈 Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Products", len(products))
    m2.metric("Orders", len(orders))
    m3.metric("Total Stock", products["stock"].sum())
