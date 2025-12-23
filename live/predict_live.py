import yfinance as yf
import pandas as pd
import ta
import joblib

# Load trained model
model = joblib.load("model/intraday_xgb.pkl")

# Fetch intraday data
data = yf.download(
    "RELIANCE.NS",
    interval="5m",
    period="5d",
    progress=False
)

# Fix MultiIndex columns if present
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data = data.reset_index()

df = data[["Datetime", "Open", "High", "Low", "Close", "Volume"]].copy()

# Ensure numeric columns
numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# Feature engineering
df["ema_9"] = ta.trend.EMAIndicator(df["Close"], window=9).ema_indicator()
df["ema_21"] = ta.trend.EMAIndicator(df["Close"], window=21).ema_indicator()
df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
df["vwap"] = (df["Volume"] * df["Close"]).cumsum() / df["Volume"].cumsum()

df.dropna(inplace=True)

# Latest candle
latest = df.iloc[-1][["ema_9", "ema_21", "rsi", "vwap"]].values.reshape(1, -1)

prediction = model.predict(latest)[0]
confidence = model.predict_proba(latest).max()

label_map = {0: "SELL", 1: "HOLD", 2: "BUY"}

print("📊 LIVE SIGNAL:", label_map[prediction])
print("📈 Confidence:", round(confidence, 2))
