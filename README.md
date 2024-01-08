# project-kafka-streaming-MAP670
This is a project of Master-DS of IPP of the course "Data Stream Processing". In this project, we will do Kafka streaming of crypto stock market (such bitcoin, ethereum, etc) and use this streaming data to applied on online learning (river). Besides, we also use Batch incremental Emsemble learning. We then compare the perfomances of these models.


# prerequirements
You need to download Apache Kafka into your system via 
https://dlcdn.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz (or visit the website https://kafka.apache.org/downloads)
then extract the tar file

You also need these python libraries: 
- river == 0.11.0
- kafka-python
- matplotlib
- yfinance
- pandas
- numpy
- scikit-learn 


# python script descriptions
- In this project, there are multiple python script, let's have a look how each one works:
    - producer.py
    this script is used to load crypto stock data from yahoo finance (yfinance library) and then send those data to different topics by producer. As we work on 3 different crypto prices such as bitcoin, ethereum, and litecoin, there are therefore 3 kafka topics that are used to send those data.

    - parameter.py
    This script just contains some parameter that might be used and shared across other python file. For example: crypto_symbol , crypto-name, or topic name. This is important as when we work on plotting stock data, or using online learning , we only focus on specific crypto currency. Therefore, we can specify/adjust the parameters in this file.

    -plot.py 
    This file is used to plot the stock data in realtime(days) along with it Moving Average of 10days. When we receive new stock data from the kafka topic by consumer, then the figure reupdate and plot the new data.

    -process_message.py
    This file contain a function called **process_kafka_message_to_model** which will be used by many other script of different model.

    - BIE.py 
    This is the batch_incremental_emsemble learning. The window_size is set to 20, meaning that the model wait until it receives 20 stock data from consumer, then there will be one LinearRegression model on that batch of stock data. After that, its evaluation metric values (RMSE, MAE, and SMAPE) will be writen to a csv file.

    - LogisticRegressor.py, PAregression.py, knnregression.py, hoeffdingTreeRegressor.py, hoeffdingAdaptiveTreeRegressor.py, AdaptiveRandomForest.py and snarimax.py

    These file are all similar. They are just different regression model. The reason why they are separated in different file is that we need to run them simultaneously when receiving new stocking. When the consumer receive a message, the script recall **process_kafka_message_to_model** from precess_message.py and run the model. After that, theirs evaluation metric values (RMSE, MAE, and SMAPE) will be writen to a csv file.

    Note: as we receive one message of stock data at a time, and it can we process once. Then we use **Open, High , Low** of each stock data as features, and **Close** of the stock data as target. This works with the batch learning and online learning regression model. However, we only use **Close** of the stock data as target for time-series model of snarimax.py

    -result.py
    This file read the evaluation metric values (RMSE, MAE, and SMAPE) of each models from csv file and then plot them.


# Step
- Before running any python script, you have to start server kafka:
    -  cd kafka_2.13-3.6.0  ( or whatever version you have, you need to locate your kafka repository)
    -  execute:
        bin/kafka-server-start.sh config/server.properties
    -  execute:
        bin/zookeeper-server-start.sh config/zookeeper.properties
- then you can run producer.py.
- you can execute plot.py in different terminal to see the evolution of the stock data.
- next, you can run all the regression python files in different terminal in parallel.
- finally, you can run result.py to see the Error value of each model.








