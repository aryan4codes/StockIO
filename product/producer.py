import yfinance as yf
import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['13.235.70.46:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# List of top 10 stock tickers
top_10_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ']

# Fetch real-time stock data from Yahoo Finance
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')
    return data.tail(1).to_dict(orient='records')[0] if not data.empty else None

# Send stock data to Kafka topic
while True:
    for ticker in top_10_tickers:
        stock_data = fetch_stock_data(ticker)
        if stock_data:
            stock_data['Ticker'] = ticker  # Add ticker symbol to data
            producer.send('stock_data', value=stock_data)
            print(f"Sent data for {ticker}: {stock_data}")
    sleep(60)  # Fetch and send data every minute
