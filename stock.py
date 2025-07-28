import streamlit as st
import yfinance as yf
import pandas as pd

def stock_page():
    st.header("Stock Data Fetcher")

    ticker = st.text_input("Enter Stock Symbol", "INFY.NS")
    period_choice = st.selectbox("Select Period", ["1y", "5y", "10y", "max"])
    interval_choice = st.selectbox("Select Interval", ["1d", "1wk", "1mo", "3mo"])

    if st.button("Show Data"):
        data = fetch_stock_data(ticker, period_choice, interval_choice)

        if data.empty:
            st.error("No data found. Please check your ticker symbol.")
        else:
            data.reset_index(inplace=True)

            # ✅ Flatten MultiIndex columns
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = [col[0] if col[0] else "Date" for col in data.columns]

            # ✅ Ensure Adj Close column exists (some intervals don’t return it)
            if "Adj Close" not in data.columns:
                data["Adj Close"] = data["Close"]

            # ✅ Keep only required columns
            data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

            # ✅ Sort latest → oldest
            data = data.sort_values(by="Date", ascending=False)

            st.dataframe(data)

            # ✅ CSV download
            csv = data.to_csv(index=False)
            st.download_button("Download CSV", csv, f"{ticker}_data.csv", "text/csv")

def fetch_stock_data(ticker, period, interval):
    try:
        return yf.download(ticker, period=period, interval=interval)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()
