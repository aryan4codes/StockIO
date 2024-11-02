# main.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch_data_from_s3
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Define top 10 tickers
top_10_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ']

# Auto-refresh every 60 seconds (60000 milliseconds)
count = st_autorefresh(interval=10 * 1000, key="main_page_refresh")

# Streamlit app layout
st.title('Real-Time Stock Market Analysis Dashboard')
st.sidebar.header('Dashboard Controls')

# Optional: Allow users to select refresh interval
# refresh_interval = st.sidebar.selectbox(
#     'Select Refresh Interval',
#     options=[30, 60, 120],
#     format_func=lambda x: f"{x} seconds"
# )
# count = st_autorefresh(interval=refresh_interval * 1000, key="main_page_refresh")

# Fetch and display data
st.write('Fetching latest stock data from S3...')
data = fetch_data_from_s3(top_10_tickers)

if not data.empty:
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data = data.sort_values(by=['Ticker', 'Datetime'])
    
    st.write(data)
    
    # Dropdown to select specific stock for detailed view
    selected_ticker = st.sidebar.selectbox('Select Stock', top_10_tickers)
    
    filtered_data = data[data['Ticker'] == selected_ticker]
    
    # Closing Prices Over Time
    st.header(f'{selected_ticker} Closing Prices Over Time')
    fig_close = px.line(filtered_data, x='Datetime', y='Close', title=f'{selected_ticker} Closing Prices Over Time')
    st.plotly_chart(fig_close, use_container_width=True)
    
    # Volume Over Time
    st.header(f'{selected_ticker} Volume Over Time')
    fig_volume = px.line(filtered_data, x='Datetime', y='Volume', title=f'{selected_ticker} Volume Over Time')
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # High-Low Price Range Over Time
    st.header(f'{selected_ticker} High-Low Price Range Over Time')
    fig_high_low = px.area(filtered_data, x='Datetime', y=['High', 'Low'], title=f'{selected_ticker} High-Low Price Range Over Time')
    st.plotly_chart(fig_high_low, use_container_width=True)
    
    # Moving Average of Closing Price
    st.header(f'{selected_ticker} Moving Average of Closing Price')
    filtered_data['MA_Close'] = filtered_data['Close'].rolling(window=10).mean()
    fig_ma_close = px.line(filtered_data, x='Datetime', y='MA_Close', title=f'10-Minute Moving Average of {selected_ticker} Closing Price')
    st.plotly_chart(fig_ma_close, use_container_width=True)
    
    # Daily Price Change
    st.header(f'{selected_ticker} Daily Price Change')
    filtered_data['Price Change'] = filtered_data['Close'] - filtered_data['Open']
    fig_price_change = px.bar(filtered_data, x='Datetime', y='Price Change', title=f'{selected_ticker} Daily Price Change')
    st.plotly_chart(fig_price_change, use_container_width=True)
    
    # Technical Indicators (e.g., RSI)
    st.header(f'{selected_ticker} Technical Indicators')
    try:
        import ta
        filtered_data['RSI'] = ta.momentum.RSIIndicator(filtered_data['Close'], window=14).rsi()
        fig_rsi = px.line(filtered_data, x='Datetime', y='RSI', title=f'{selected_ticker} RSI Over Time')
        st.plotly_chart(fig_rsi, use_container_width=True)
    except ImportError:
        st.write("Install the 'ta' library for technical indicators: `pip install ta`")
    
else:
    st.write('No data available yet.')
