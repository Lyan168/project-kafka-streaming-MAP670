import json
import csv

def process_kafka_message_to_model(message, model, metrics,csv_file_path, print_progress=False):
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)
    
    # Assuming data is a tuple or similar structure containing features (x) and target (y)
    date= data["date"]
    y = data["Close"] 
    del data["Close"] 
    del data["date"] 
    x = data

    # Predict
    y_pred = model.predict_one(x)

    # Update metrics
    for i,metric in enumerate(metrics):
        metric.update(y_true=y, y_pred=y_pred)
    # metrics.update(y_true=y, y_pred=y_pred)

    # Check if it's time to print progress
    if print_progress:
        print(metrics,'\n')
    
    # Learn (train)
    model.learn_one(x, y)

    new_data = [model.__class__.__name__,date, metrics[0].get(), metrics[1].get(), metrics[2].get()]
    # print(new_data)

    with open(csv_file_path, mode='a', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the new line to the CSV file
        csv_writer.writerow(new_data)
