import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE SETTINGS
st.set_page_config(layout="wide", page_title="E-Commerce AI Dashboard")

# LOAD CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# LOAD DATA
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")

# TITLE
st.markdown("<h1>🛒 E-Commerce AI Chatbot Dashboard</h1>", unsafe_allow_html=True)

# ---------------- TOP ROW ----------------
col1, col2 = st.columns(2)

# TABLE LEFT
with col1:
    st.subheader("📦 Products Table")
    st.table(products)   # NO SCROLL TABLE

# CHART RIGHT
with col2:
    st.subheader("📊 Stock Chart")

    fig, ax = plt.subplots(figsize=(6,3))
    ax.bar(products["product"], products["stock"])
    ax.set_ylabel("Stock")
    ax.set_title("Product Stock Levels")
    st.pyplot(fig)

# ---------------- BOTTOM ROW ----------------
col3, col4 = st.columns(2)

# CHATBOT LEFT
with col3:
    st.subheader("🤖 Chatbot")
    user_input = st.text_input("Ask product price or track order")

    reply = ""

    if user_input:
        user_input = user_input.lower()

        # Price Query
        for p in products["product"]:
            if p.lower() in user_input and "price" in user_input:
                price = products[products["product"] == p]["price"].values[0]
                reply = f"{p} price is ₹{price}"

        # Order Tracking
        if "track" in user_input or "order" in user_input:
            for order_id in orders["order_id"].astype(str):
                if order_id in user_input:
                    status = orders[orders["order_id"] == int(order_id)]["status"].values[0]
                    reply = f"Order {order_id} status: {status}"

        if reply == "":
            reply = "I can show product prices and track orders 😊"

        st.markdown(f"<div class='chatbox'>🤖 {reply}</div>", unsafe_allow_html=True)

# SUMMARY RIGHT
with col4:
    st.subheader("📈 Business Summary")

    m1, m2, m3 = st.columns(3)
    m1.metric("Products", len(products))
    m2.metric("Orders", len(orders))
    m3.metric("Total Stock", products["stock"].sum())