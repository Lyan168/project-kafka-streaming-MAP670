from river import metrics
from river.stream import iter_pandas
from river.neighbors import KNNRegressor
from kafka import KafkaConsumer
import json
import os
import csv

from parameter import crypto_symbol, historical_topic, crypto_name, topic_to_use
from process_message import process_kafka_message_to_model

###############################################

# Create a consumer instance
consumer = KafkaConsumer(
    topic_to_use,
    bootstrap_servers='localhost:9092',
     
)

# Initialize metrics and model outside the loop
rmse = metrics.RMSE()
mae = metrics.MAE()
smape = metrics.SMAPE()

metrics_list = [ rmse, mae, smape]

counter=0
n_wait=5
is_print= False

knn = KNNRegressor()

for message in consumer:
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)

    csv_file_path = f'./Metrics/{knn.__class__.__name__}_metrics.csv'
    if counter == 0:
        directory = os.path.dirname(csv_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["model","date", "RMSE","MAE","SMAPE"])  
    
    if counter % n_wait == 0 and counter > 0:
        is_print= True
    process_kafka_message_to_model(message , knn, metrics_list, csv_file_path, is_print)
    is_print= False
    counter+=1




    
