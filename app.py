import streamlit as st
import pandas as pd

# FULL SCREEN WIDE MODE
st.set_page_config(layout="wide", page_title="E-Commerce Dashboard")

# REMOVE STREAMLIT SCROLL & PADDING
st.markdown("""
<style>
.main {
    padding: 0px !important;
}
.block-container {
    padding-top: 10px !important;
    padding-bottom: 0px !important;
}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load Data
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")

# TITLE
st.markdown("<h2 style='text-align:center;'>🛒 E-Commerce AI Chatbot Dashboard</h2>", unsafe_allow_html=True)

# -------- TOP ROW --------
col1, col2 = st.columns(2)

# TABLE
with col1:
    st.subheader("📦 Products Table")
    st.dataframe(products, use_container_width=True, height=250)

# CHART
with col2:
    st.subheader("📊 Stock Chart")
    st.bar_chart(products.set_index("product")["stock"], height=250, use_container_width=True)

# -------- BOTTOM ROW --------
col3, col4 = st.columns(2)

# CHATBOT
with col3:
    st.subheader("🤖 Chatbot")
    user_input = st.text_input("Ask product price or order tracking")

    reply = "Ask me product price or order tracking 😊"

    if user_input:
        user_input = user_input.lower()

        # Price Query
        for p in products["product"]:
            if p.lower() in user_input and "price" in user_input:
                price = products.loc[products["product"] == p, "price"].values[0]
                reply = f"{p} price is ₹{price}"

        # Order Tracking
        if "track" in user_input or "order" in user_input:
            for oid in orders["order_id"].astype(str):
                if oid in user_input:
                    status = orders.loc[orders["order_id"] == int(oid), "status"].values[0]
                    reply = f"Order {oid} status: {status}"

    st.success(reply)

# BUSINESS SUMMARY
with col4:
    st.subheader("📈 Summary")

    m1, m2, m3 = st.columns(3)
    m1.metric("Products", len(products))
    m2.metric("Orders", len(orders))
    m3.metric("Total Stock", products["stock"].sum())
