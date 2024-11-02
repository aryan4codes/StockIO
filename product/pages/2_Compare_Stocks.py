# pages/2_Compare_Stocks.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch_data_from_s3
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Define top 10 tickers
top_10_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ']

# Auto-refresh every 60 seconds (60000 milliseconds)
count = st_autorefresh(interval=10 * 1000, key="compare_page_refresh")

# Streamlit page layout
st.title('Comparative Analysis of Top 10 Stocks')

# Optional: Allow users to select refresh interval
# refresh_interval = st.sidebar.selectbox(
#     'Select Refresh Interval',
#     options=[30, 60, 120],
#     format_func=lambda x: f"{x} seconds"
# )
# count = st_autorefresh(interval=refresh_interval * 1000, key="compare_page_refresh")

# Fetch and display data
st.write('Fetching latest stock data from S3...')
data = fetch_data_from_s3(top_10_tickers)

if not data.empty:
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data = data.sort_values(by=['Ticker', 'Datetime'])
    
    # Pivot data for comparative analysis
    pivot_close = data.pivot_table(index='Datetime', columns='Ticker', values='Close')
    pivot_volume = data.pivot_table(index='Datetime', columns='Ticker', values='Volume')
    
    # Comparative Closing Prices
    st.header('Comparative Closing Prices Over Time')
    fig_compare_close = px.line(pivot_close, x=pivot_close.index, y=pivot_close.columns, title='Closing Prices Comparison')
    st.plotly_chart(fig_compare_close, use_container_width=True)
    
    # Comparative Volume
    st.header('Comparative Volume Over Time')
    fig_compare_volume = px.bar(pivot_volume, x=pivot_volume.index, y=pivot_volume.columns, title='Volume Comparison')
    st.plotly_chart(fig_compare_volume, use_container_width=True)
    
    # Correlation Matrix of Closing Prices
    st.header('Correlation Matrix of Closing Prices')
    correlation = pivot_close.corr()
    fig_corr = px.imshow(correlation, text_auto=True, title='Correlation Matrix of Closing Prices')
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Cumulative Returns
    st.header('Cumulative Returns Over Time')
    cumulative_returns = (pivot_close / pivot_close.iloc[0] - 1) * 100
    fig_cum_returns = px.line(cumulative_returns, x=cumulative_returns.index, y=cumulative_returns.columns, title='Cumulative Returns (%)')
    st.plotly_chart(fig_cum_returns, use_container_width=True)
    
    # Volatility Comparison
    st.header('Volatility Comparison')
    returns = pivot_close.pct_change()
    volatility = returns.std() * (60**0.5)  # Assuming data is per minute; adjust scaling as needed
    fig_volatility = px.bar(volatility, x=volatility.index, y=volatility.values, title='Volatility (Std Dev of Returns)')
    st.plotly_chart(fig_volatility, use_container_width=True)
    
    # Moving Averages for all stocks
    st.header('Moving Averages')
    moving_avg = pivot_close.rolling(window=10).mean()
    fig_ma = px.line(moving_avg, x=moving_avg.index, y=moving_avg.columns, title='10-Minute Moving Averages of Closing Prices')
    st.plotly_chart(fig_ma, use_container_width=True)
    
    # Top Gainers and Losers
    st.header('Top Gainers and Losers')
    latest_data = data.sort_values(by='Datetime').groupby('Ticker').tail(1)
    latest_data['Price Change'] = latest_data['Close'] - latest_data['Open']
    top_gainers = latest_data.nlargest(5, 'Price Change')
    top_losers = latest_data.nsmallest(5, 'Price Change')
    
    st.subheader('Top Gainers')
    st.write(top_gainers[['Ticker', 'Price Change']])
    
    st.subheader('Top Losers')
    st.write(top_losers[['Ticker', 'Price Change']])
    
    # Performance Metrics
    st.header('Performance Metrics')
    performance_metrics = latest_data.copy()
    performance_metrics['Percentage Change'] = (performance_metrics['Close'] - performance_metrics['Open']) / performance_metrics['Open'] * 100
    fig_perf = px.bar(performance_metrics, x='Ticker', y='Percentage Change', title='Percentage Change of Stocks')
    st.plotly_chart(fig_perf, use_container_width=True)
    
    # Heatmap of Correlations
    st.header('Heatmap of Correlations')
    fig_heatmap = px.imshow(correlation, text_auto=True, title='Heatmap of Closing Price Correlations')
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Portfolio Analysis (Example: Equal-Weighted Portfolio)
    st.header('Portfolio Analysis')
    portfolio = pivot_close.mean(axis=1)
    portfolio.name = 'Equal-Weighted Portfolio'
    fig_portfolio = px.line(portfolio, x=portfolio.index, y=portfolio.values, title='Equal-Weighted Portfolio Closing Price')
    st.plotly_chart(fig_portfolio, use_container_width=True)
    
else:
    st.write('No data available yet.')
