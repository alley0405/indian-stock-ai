import pandas as pd
import ta

df = pd.read_csv("data/reliance_5min.csv")

# 🔹 Fix timestamp column automatically
if 'Datetime' in df.columns:
    time_col = 'Datetime'
elif 'Date' in df.columns:
    time_col = 'Date'
else:
    time_col = df.columns[0]  # fallback (index column)

df.rename(columns={time_col: 'Datetime'}, inplace=True)

# 🔹 Keep only required columns
df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]

# 🔹 Convert to numeric safely
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

# 🔹 Indicators
df['ema_9'] = ta.trend.EMAIndicator(df['Close'], window=9).ema_indicator()
df['ema_21'] = ta.trend.EMAIndicator(df['Close'], window=21).ema_indicator()
df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
df['vwap'] = ta.volume.VolumeWeightedAveragePrice(
    df['High'], df['Low'], df['Close'], df['Volume']
).volume_weighted_average_price()

df.dropna(inplace=True)

df.to_csv("data/reliance_5min_features.csv", index=False)

print("✅ Intraday features generated successfully")
