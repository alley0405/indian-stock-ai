import yfinance as yf
import os

def fetch_intraday(symbol):
    df = yf.download(
        symbol,
        interval="5m",
        period="7d"
    )
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = fetch_intraday("RELIANCE.NS")
    df.to_csv("data/reliance_5min.csv")
    print("✅ 5-minute intraday data saved")
