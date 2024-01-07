
import locale
from kafka import KafkaConsumer
import json
from datetime import datetime
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from parameter import crypto_symbol, historical_topic, crypto_name

# Create a consumer instance
consumer = KafkaConsumer(
    historical_topic,
    bootstrap_servers='localhost:9092',
)
consumer2 = KafkaConsumer(
    'historical-LTC-USD-topic',
    bootstrap_servers='localhost:9092',
)

timestamps = []
prices = []

def plot_time_series(message,  name_crypto, window_size=10):

    rounded_value = round(message['Close'])            # Round the value to the nearest dollar

    timestamps.append(datetime.strptime(message['date'],'%Y-%m-%d'))
    prices.append(rounded_value)

    # Create a pandas DataFrame with timestamps and prices
    df = pd.DataFrame({'Timestamp': timestamps, 'Price': prices})

    # Calculate the (window_size)-period moving average of the Bitcoin price
    df['MA'] = df['Price'].rolling(window=window_size).mean()

    # Clear the previous plot
    plt.clf()

    # Plot the Bitcoin prices and moving average over time
    plt.plot(df['Timestamp'], df['Price'], label='Bitcoin Price')
    plt.plot(df['Timestamp'], df['MA'], label=f'Moving Average ({window_size} days)')
    plt.xlabel('Time')
    plt.ylabel(f'{name_crypto} Price (USD)')
    plt.xticks(rotation=45)  # Adjust the angle as needed
    plt.title(f'Historical {name_crypto} Price with Moving Average')
    plt.legend()

    # Adjust the plot margins
    plt.gcf().autofmt_xdate()

    # Display the plot
    plt.pause(0.001)



# Start consuming
for message in consumer2:
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)

    plot_time_series(data, name_crypto=crypto_name)

    

    
