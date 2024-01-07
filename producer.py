from time import sleep
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from kafka import KafkaProducer
import json

def get_crypto_data(date, symbol):
    
    current_date_str = date.strftime("%Y-%m-%d")
    next_date = date + timedelta(days=1)
    next_date_str = next_date.strftime("%Y-%m-%d")

    ticker_symbol = symbol
    crypto_data = yf.download(ticker_symbol,start=current_date_str, end=next_date_str)

    print(crypto_data)

    if not crypto_data.empty:
        return {'date' : crypto_data.index[0].strftime('%Y-%m-%d'),
                'Close' : crypto_data["Close"][0],
                'Open' : crypto_data["Open"][0],
                'High' : crypto_data["High"][0],
                'Low' : crypto_data["Low"][0],
                }
    else:
        print(f"Error retrieving price")
        return None


####################################################################################################
# Create a producer instance
producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda v: json.dumps(v).encode('utf-8'))


crypto_symbols = ["BTC-USD", "ETH-USD","LTC-USD"]
topics = ["historical-BTC-USD-topic", "historical-ETH-USD-topic","historical-LTC-USD-topic"]

start_date = "2022-01-01"
start_date = datetime.strptime(start_date, "%Y-%m-%d")

# Get today's date
end_date = datetime.today()

# Create a while loop to fetch data for each day
current_date = start_date
while current_date < end_date:
    
    # Get Bitcoin data for the current date
    for crypto_symbol, topic in zip(crypto_symbols, topics):
        data = get_crypto_data(current_date, crypto_symbol)
        producer.send(topic, data)

        # Print or process the fetched data as needed
        print(f"Data for {crypto_symbol} on {current_date}:\n{data}\n")

    
    current_date += timedelta(days=1)
    sleep(0.5)







