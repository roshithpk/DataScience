import streamlit as st
import yfinance as yf
import pandas as pd

def stock_page():
    st.header("Stock Data Fetcher")

    ticker = st.text_input("Enter Stock Symbol", "INFY")
    period_choice = st.selectbox("Select Period", ["1y", "5y", "10y", "max"])
    interval_choice = st.selectbox("Select Interval", ["1d", "1wk", "1mo", "3mo"])

    if st.button("Download Stock Data"):
        data = fetch_stock_data(ticker, period_choice, interval_choice)
        if data.empty:
            st.error("No data found. Please check your ticker symbol.")
        else:
            st.dataframe(data)
            csv = data.to_csv()
            st.download_button("Download CSV", csv, f"{ticker}_data.csv", "text/csv")

def fetch_stock_data(ticker, period, interval):
    try:
        return yf.download(ticker, period=period, interval=interval)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

