import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import joblib

st.set_page_config(page_title="Indian Stock AI", layout="wide")

st.title("📈 Indian Stock AI – Intraday Predictor")
st.caption("AI-based BUY / SELL / HOLD signals using real-time market data")

# Load model
model = joblib.load("model/intraday_xgb.pkl")

symbol = st.selectbox(
    "Select Stock",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
)

# Fetch data
data = yf.download(
    symbol,
    interval="5m",
    period="5d",
    progress=False
)

# Fix MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.reset_index(inplace=True)

df = data[["Datetime", "Open", "High", "Low", "Close", "Volume"]].copy()
df[["Open", "High", "Low", "Close", "Volume"]] = df[
    ["Open", "High", "Low", "Close", "Volume"]
].apply(pd.to_numeric, errors="coerce")

# Features
df["ema_9"] = ta.trend.EMAIndicator(df["Close"], window=9).ema_indicator()
df["ema_21"] = ta.trend.EMAIndicator(df["Close"], window=21).ema_indicator()
df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
df["vwap"] = (df["Volume"] * df["Close"]).cumsum() / df["Volume"].cumsum()

df.dropna(inplace=True)

# AI Prediction
latest = df.iloc[-1][["ema_9", "ema_21", "rsi", "vwap"]].values.reshape(1, -1)
pred = model.predict(latest)[0]
confidence = model.predict_proba(latest).max()

label_map = {0: "SELL 🔴", 1: "HOLD 🟡", 2: "BUY 🟢"}

st.subheader("📊 AI Signal")
st.metric("Prediction", label_map[pred])
st.metric("Confidence", f"{confidence:.2f}")

# Chart
st.subheader("📉 Intraday Price Chart")
st.line_chart(df.set_index("Datetime")[["Close", "ema_9", "ema_21"]])

# RSI
st.subheader("📐 RSI Indicator")
st.line_chart(df.set_index("Datetime")[["rsi"]])
