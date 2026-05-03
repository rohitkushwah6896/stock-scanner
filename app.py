import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

# App Configuration
st.set_page_config(page_title="Stock Scanner", layout="wide")
st.title("📈 Stock Pattern & Volume Scanner")

# User Input
ticker = st.sidebar.text_input("Enter Ticker (e.g., SUZLON.NS, IRFC.NS)", "SUZLON.NS")

if ticker:
    try:
        df = yf.download(ticker, period="1y", interval="1d")
        if not df.empty:
            # Technical Indicators
            df['SMA21'] = ta.sma(df['Close'], length=21)
            df['SMA50'] = ta.sma(df['Close'], length=50)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            
            # Show Price Metric
            st.metric("Current Price", f"₹{df['Close'].iloc[-1]:.2f}")
            
            # Candlestick Chart
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA21'], name='SMA 21', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name='SMA 50', line=dict(color='red')))
            fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Simple Pattern Alert (Similar to your screenshot)
            st.subheader("Analysis Signals")
            if df['SMA21'].iloc[-1] > df['SMA50'].iloc[-1]:
                st.success("🟢 Bullish Signal: SMA 21 is above SMA 50")
            else:
                st.error("🔴 Bearish Signal: SMA 21 is below SMA 50")
    except:
        st.error("Please enter a valid ticker.")
