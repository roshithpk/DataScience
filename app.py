import streamlit as st
from stock import stock_page

st.title("Stock & Gold Price Data Fetcher")

menu = st.selectbox("Select Data Type", ["Stock"])  # For now only Stock

if menu == "Stock":
    stock_page()

