import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #ff4b5c, #ff758c, #5f2c82, #00c6ff);
    background-attachment: fixed;
}

/* Fix Heading Cut Issue */
.block-container {
    padding-top: 80px !important;
}

/* Title Style */
h1 {
    color: white !important;
    text-align: center;
    font-size: 40px !important;
    font-weight: bold;
}

/* Table Background */
.stDataFrame {
    background-color: rgba(255,255,255,0.25);
    border-radius: 12px;
}

/* Chart Background */
canvas {
    background-color: white;
    border-radius: 12px;
}

/* Metrics Cards */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.25);
    padding: 15px;
    border-radius: 15px;
    color: white;
}

/* Input Box */
.stTextInput input {
    background-color: rgba(255,255,255,0.25);
    color: black;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
products = pd.DataFrame({
    "product": ["Laptop", "Mobile", "Headphones", "Smart Watch", "Camera"],
    "price": [55000, 15000, 2000, 3500, 45000],
    "stock": [10, 25, 50, 30, 5]
})

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104],
    "status": ["Delivered", "Shipped", "Processing", "Cancelled"]
})

# ---------- TITLE ----------
st.title("🛒 E-Commerce AI Chatbot Dashboard")

# ---------- TOP ROW ----------
col1, col2 = st.columns([1,1])

# TABLE
with col1:
    st.subheader("📦 Products Table")
    st.dataframe(products, height=300, use_container_width=True)

# CHART
with col2:
    st.subheader("📊 Stock Chart")
    st.bar_chart(products.set_index("product")["stock"], height=300)

# ---------- BOTTOM ROW ----------
col3, col4 = st.columns([1,1])

# CHATBOT
with col3:
    st.subheader("🤖 Chatbot")
    user_input = st.text_input("Ask product price or track order")

    reply = "I can show product prices and track orders 😊"

    if user_input:
        text = user_input.lower()

        # Price Query
        for p in products["product"]:
            if p.lower() in text and "price" in text:
                price = products[products["product"] == p]["price"].values[0]
                reply = f"{p} price is ₹{price}"

        # Order Tracking
        if "order" in text or "track" in text:
            for oid in orders["order_id"].astype(str):
                if oid in text:
                    status = orders[orders["order_id"] == int(oid)]["status"].values[0]
                    reply = f"Order {oid} status: {status}"

    st.success(reply)

# SUMMARY
with col4:
    st.subheader("📈 Business Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Products", len(products))
    m2.metric("Orders", len(orders))
    m3.metric("Total Stock", products["stock"].sum())

