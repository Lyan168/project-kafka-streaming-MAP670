from river import metrics
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from kafka import KafkaConsumer
import json
from river.utils import dict2numpy
import csv
import os

from parameter import crypto_symbol, topic, crypto_name
from process_message import process_kafka_message_to_model

###############################################
class BatchRegressor:

    def __init__(self, window_size=20, max_models=20):
        self.H = []
        self.h = None

        self.window_size = window_size
        self.max_models = max_models
        self.X_batch = []
        self.Y_batch = []

    def learn_one(self, x, y=None):
        if self.h is None:
            # self.h = LogisticRegression()
            self.h = LinearRegression()
            # self.h = KNeighborsRegressor(n_neighbors=5)
        
        x_np = dict2numpy(x)
        # y_np = dict2numpy(y)

        self.X_batch.append(x_np)
        self.Y_batch.append(y)


        if len(self.X_batch)== self.window_size:
            # h = LogisticRegression()
            h = LinearRegression()
            # h = KNeighborsRegressor(n_neighbors=5)

            h.fit(self.X_batch, self.Y_batch)
            self.H.append(h)
            self.X_batch.clear()
            self.Y_batch.clear()
        
        if len(self.H) > self.max_models:
            self.H.pop(0)

        return self

    def predict_one(self, x):

        result=[]
        x_np = dict2numpy(x).reshape(1, -1)

        if len(self.H) == 0:
            return 0
        else:
            for h in self.H:
                res=h.predict(x_np)
                result.append(res)
        
        final_res= sum(result) / len(result)
        return final_res[0]

###############################################

# Create a consumer instance
consumer = KafkaConsumer(
    topic,
    bootstrap_servers='localhost:9092',  
)

# Initialize metrics 
rmse = metrics.RMSE()
mae = metrics.MAE()
smape = metrics.SMAPE()

metrics_list = [ rmse, mae, smape]

counter=0
n_wait=5
is_print= False

bie= BatchRegressor(window_size=20, max_models=20)

# Start consuming
for message in consumer:
    decoded_message = message.value.decode('utf-8')
    data = json.loads(decoded_message)
    
    #check if the directory exists, if no, create it, 
    #then if the csv file exists, overwrite the previous content with just header
    csv_file_path = f'./Metrics/{bie.__class__.__name__}_metrics.csv'
    if counter == 0:
        directory = os.path.dirname(csv_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["model","date", "RMSE","MAE","SMAPE"])  
      

    if counter % n_wait == 0 and counter > 0:
        is_print= True
    process_kafka_message_to_model(message , bie, metrics_list,csv_file_path, is_print)
    is_print= False
    counter+=1



