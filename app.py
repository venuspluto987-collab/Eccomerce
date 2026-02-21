import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ff4b5c, #ff758c, #5f2c82, #00c6ff);
    background-attachment: fixed;
}

.block-container {
    padding-top: 50px !important;
}

h1, h2, h3 {
    color: white !important;
}

/* Card Style */
.card {
    background: rgba(255,255,255,0.25);
    padding: 20px;
    border-radius: 15px;
}

/* Input */
.stTextInput input {
    background: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
products = pd.DataFrame({
    "product": ["Laptop", "Mobile", "Headphones", "Smart Watch", "Camera"],
    "price": [55000, 15000, 2000, 3500, 45000],
    "stock": [10, 25, 50, 30, 5]
})

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104],
    "status": ["Delivered", "Shipped", "Processing", "Cancelled"]
})

# ---------- TOP NAV BAR ----------
selected = option_menu(
    menu_title="🛒 E-Commerce AI Dashboard",
    options=["Products Table", "Stock Chart", "Chatbot", "Summary"],
    icons=["table", "bar-chart", "robot", "graph-up"],
    menu_icon="shop",
    default_index=0,
    orientation="horizontal",
)

# ---------- PRODUCTS TABLE ----------
if selected == "Products Table":
    st.markdown("<h2>📦 Products Table</h2>", unsafe_allow_html=True)
    st.dataframe(products, height=350, use_container_width=True)

# ---------- STOCK CHART ----------
if selected == "Stock Chart":
    st.markdown("<h2>📊 Product Stock Chart</h2>", unsafe_allow_html=True)
    st.bar_chart(products.set_index("product")["stock"], height=350)

# ---------- CHATBOT ----------
if selected == "Chatbot":
    st.markdown("<h2>🤖 E-Commerce Chatbot</h2>", unsafe_allow_html=True)

    user_input = st.text_input("Ask product price or track order")

    reply = "I can show product prices and track orders 😊"

    if user_input:
        text = user_input.lower()

        # Price
        for p in products["product"]:
            if p.lower() in text and "price" in text:
                price = products[products["product"] == p]["price"].values[0]
                reply = f"{p} price is ₹{price}"

        # Order tracking
        if "order" in text or "track" in text:
            for oid in orders["order_id"].astype(str):
                if oid in text:
                    status = orders[orders["order_id"] == int(oid)]["status"].values[0]
                    reply = f"Order {oid} status: {status}"

    st.success(reply)

# ---------- SUMMARY ----------
if selected == "Summary":
    st.markdown("<h2>📈 Business Summary</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", len(products))
    col2.metric("Total Orders", len(orders))
    col3.metric("Total Stock", products["stock"].sum())
