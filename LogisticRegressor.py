from river import metrics
from river.linear_model import LogisticRegression
from kafka import KafkaConsumer
import json
import os
import csv

from parameter import crypto_symbol, topic, crypto_name
from process_message import process_kafka_message_to_model

###############################################

# Create a consumer instance
consumer = KafkaConsumer(
    topic,
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

logistic = LogisticRegression()


for message in consumer:
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)

    #check if the directory exists, if no, create it, 
    #then if the csv file exists, overwrite the previous content with just header
    csv_file_path = f'./Metrics/{logistic.__class__.__name__}_metrics.csv'
    if counter == 0:
        directory = os.path.dirname(csv_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["model","date", "RMSE","MAE","SMAPE"])  
    
    if counter % n_wait == 0 and counter > 0:
        is_print= True
    process_kafka_message_to_model(message , logistic, metrics_list, csv_file_path, is_print)
    is_print= False
    counter+=1




    
