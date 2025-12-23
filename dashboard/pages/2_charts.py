import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.title("📉 Technical Charts")

symbol = st.selectbox(
    "Select Stock",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
)

data = yf.download(
    symbol,
    interval="5m",
    period="5d",
    progress=False
)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.reset_index(inplace=True)

df = data[["Datetime", "Close", "Volume"]].copy()
df["ema_9"] = ta.trend.EMAIndicator(df["Close"], window=9).ema_indicator()
df["ema_21"] = ta.trend.EMAIndicator(df["Close"], window=21).ema_indicator()
df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

df.dropna(inplace=True)

st.subheader("Price & EMA")
st.line_chart(df.set_index("Datetime")[["Close", "ema_9", "ema_21"]])

st.subheader("RSI")
st.line_chart(df.set_index("Datetime")[["rsi"]])
