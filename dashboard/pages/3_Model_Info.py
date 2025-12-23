import streamlit as st

st.title("🤖 Model Information")

st.markdown("""
### 🔍 Model Overview
- **Algorithm:** XGBoost Classifier
- **Type:** Multi-class classification
- **Classes:** BUY, HOLD, SELL

### 📊 Features Used
- EMA (9)
- EMA (21)
- RSI (14)
- VWAP

### 🎯 Prediction Logic
- Predicts short-term intraday movement
- Designed for **5-minute candles**
- Uses probability-based confidence

### 🚀 Future Enhancements
- Zerodha Kite WebSocket
- LSTM / Transformer models
- Trade execution automation
""")
