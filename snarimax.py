from river import metrics
from river import time_series
from kafka import KafkaConsumer
import json
from river import linear_model
from river import optim
import os
import csv

from parameter import crypto_symbol, topic, crypto_name

def process_kafka_message_to_model(message, model, metrics,csv_file_path, print_progress=False):
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)

    date =data["date"]
    y = data["Close"] 
    x =data["date"]
    # x =  datetime.strptime(data["date"], "%Y-%m-%d")

    # Predict
    y_pred = model.forecast(horizon=1)

    # Update metrics
    for i,metric in enumerate(metrics):
        metric.update(y_true=y, y_pred=y_pred[0])

    # Check if it's time to print progress
    if print_progress:
        print(model)
        print(metrics,'\n')
    
    # Learn (train)
    model.learn_one(y)

    new_data = [model.__class__.__name__,date, metrics[0].get(), metrics[1].get(), metrics[2].get()]

    with open(csv_file_path, mode='a', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the new line to the CSV file
        csv_writer.writerow(new_data)


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

model = (
        time_series.SNARIMAX(
                            p=15,d=0,q=0,
                            regressor=(
                            linear_model.LinearRegression(
                            intercept_init=110,
                            optimizer=optim.SGD(0.01),
                            intercept_lr=0.3))))

# Start consuming

for message in consumer:
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)

    csv_file_path = f'./Metrics/{model.__class__.__name__}_metrics.csv'
    if counter == 0:
        directory = os.path.dirname(csv_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["model","date", "RMSE","MAE","SMAPE"]) 
    
    if counter % n_wait == 0 and counter > 0:
        is_print= True
    process_kafka_message_to_model(message , model, metrics_list, csv_file_path, is_print)
    is_print= False
    counter+=1
