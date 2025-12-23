import pandas as pd

df = pd.read_csv("data/reliance_5min_features.csv")

# Predict 3 candles ahead
df['future_close'] = df['Close'].shift(-3)
df['return'] = (df['future_close'] - df['Close']) / df['Close']

def label_trade(r):
    if r > 0.0025:
        return 1      # BUY
    elif r < -0.0025:
        return -1     # SELL
    else:
        return 0      # HOLD

df['signal'] = df['return'].apply(label_trade)

df.dropna(inplace=True)
df.to_csv("data/reliance_labeled.csv", index=False)

print("✅ Labels created successfully")
