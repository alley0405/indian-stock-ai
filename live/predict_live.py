import pandas as pd
import ta
import joblib

MODEL_PATH = "model/intraday_xgb.pkl"
DATA_PATH = "data/reliance_5min.csv"

# ===============================
# Load trained model
# ===============================
model = joblib.load(MODEL_PATH)

# ===============================
# Load latest intraday data
# ===============================
df = pd.read_csv(DATA_PATH)

# Fix timestamp column
if "Datetime" not in df.columns:
    df.rename(columns={df.columns[0]: "Datetime"}, inplace=True)

# Keep only required columns
df = df[["Datetime", "Open", "High", "Low", "Close", "Volume"]]

# 🔴 FORCE numeric conversion (CRITICAL FIX)
for col in ["Open", "High", "Low", "Close", "Volume"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop invalid rows
df.dropna(inplace=True)

# Take enough rows for indicators
df = df.tail(50).copy()

# ===============================
# Feature engineering (MATCH TRAINING)
# ===============================
df["ema_9"] = ta.trend.EMAIndicator(df["Close"], window=9).ema_indicator()
df["ema_21"] = ta.trend.EMAIndicator(df["Close"], window=21).ema_indicator()
df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
df["vwap"] = ta.volume.VolumeWeightedAveragePrice(
    df["High"], df["Low"], df["Close"], df["Volume"]
).volume_weighted_average_price()

df.dropna(inplace=True)

# ===============================
# Prepare latest candle
# ===============================
latest = df.iloc[-1][["ema_9", "ema_21", "rsi", "vwap"]].values.reshape(1, -1)

# ===============================
# Predict signal
# ===============================
pred = model.predict(latest)[0]

signal_map = {
    0: "SELL",
    1: "HOLD",
    2: "BUY"
}

print("📊 Live AI Signal:", signal_map[pred])
