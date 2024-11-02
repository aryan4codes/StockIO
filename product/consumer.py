import json
from kafka import KafkaConsumer
from json import loads
from s3fs import S3FileSystem

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'stock_data',
    bootstrap_servers=['13.235.70.46:9092'],
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

# Initialize S3 file system
s3 = S3FileSystem()

# Consume data from Kafka topic and save to S3 bucket
for count, message in enumerate(consumer):
    ticker = message.value.get('Ticker', 'unknown')
    with s3.open(f's3://stockio-dods/{ticker}/stock_market_{count}.json', 'w') as file:
        json.dump(message.value, file)
    print(f"Saved data to S3: {ticker}/stock_market_{count}.json")
