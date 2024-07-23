# StockIO: Real-Time Stock Market Data Streaming and Analysis with Kafka and AWS
*StockIO is a real-time data streaming solution designed to process and analyze stock market data using Apache Kafka and AWS services.*

![Architecture Design](https://github.com/user-attachments/assets/75976cef-ac0b-4b1e-aa2b-fe987bc02cd4)


## Project Overview

StockIO is a real-time streaming application that simulates stock market data and processes it using Apache Kafka and various AWS services.
- Hosted on AWS EC2
- The processed data is stored in Amazon S3
- Analyzed using AWS Glue and Amazon Athena.

## Data:

1. **Ensure the stock market dataset is available:**
   - Make sure you have access to the Kaggle Stock Market Dataset with the following features:
   - Dataset is given in /data folder.
     - `Index`
     - `Date`
     - `Open`
     - `High`
     - `Low`
     - `Close`
     - `Adj Close`
     - `Volume`
     - `CloseUSD`

2. **Implement the sleep function:**
   - To simulate the real-time data flow into Kafka, the producer script should include a sleep function. This will introduce delays between sending each data entry, mimicking real-time data streaming.

3. **Execute the producer script:**
   - Run the script that sends data to the Kafka topic, with the sleep function applied.
  
4. **Execute the consumer script:**
   - Run the script that reads data from the Kafka topic and stores it in S3.


## Architecture

The project architecture is designed to handle real-time stock market data and process it efficiently using the following components:

1. **Producer**: Simulates stock market data and sends it to a Kafka topic.
2. **Kafka**: Acts as the message broker to handle the stream of data.
3. **Consumer**: Reads data from the Kafka topic and stores it in Amazon S3.
4. **AWS S3**: Stores the processed stock market data.
5. **AWS Glue**: Crawls the data in S3 to create a metadata catalog.
6. **Amazon Athena**: Queries and analyzes the data stored in S3.



## How to Run the Project

### Set up Kafka on AWS EC2

1. **Launch an EC2 instance and install Kafka:**
   - Follow the instructions provided by Kafka to install it on your EC2 instance.

2. **Start the Kafka server:**
   - Use the command to start the Kafka server, usually something like `bin/kafka-server-start.sh config/server.properties`.

### Run the Producer

1. **Ensure the stock market dataset is available:**
   - Make sure you have access to the dataset required for the producer script.

2. **Execute the producer script:**
   - Run the script that sends data to the Kafka topic.

### Run the Consumer

1. **Execute the consumer script:**
   - Run the script that reads data from the Kafka topic and stores it in S3.

### Set up AWS Glue

1. **Create a Glue crawler:**
   - Configure the Glue crawler to crawl the S3 bucket and create a metadata catalog.

### Query Data with Amazon Athena

1. **Use Athena to query the data:**
   - Utilize Amazon Athena to run queries on the data stored in S3.

### Dependencies

- `pandas`
- `kafka-python`
- `s3fs`
- `boto3`
