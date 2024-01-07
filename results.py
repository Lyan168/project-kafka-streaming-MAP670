
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep

while True:

    batch_result_df = pd.read_csv("./Metrics/BatchRegressor_metrics.csv")
    knn_result_df = pd.read_csv("./Metrics/KNNRegressor_metrics.csv")
    logistic_result_df = pd.read_csv("./Metrics/LogisticRegression_metrics.csv")
    pa_results_df = pd.read_csv("./Metrics/PARegressor_metrics.csv")
    ht_result_df = pd.read_csv("./Metrics/HoeffdingTreeRegressor_metrics.csv")
    hat_result_df = pd.read_csv("./Metrics/HoeffdingAdaptiveTreeRegressor_metrics.csv")
    arf_results_df = pd.read_csv("./Metrics/AdaptiveRandomForestRegressor_metrics.csv")
    snarimax_results_df = pd.read_csv("./Metrics/SNARIMAX_metrics.csv")

    # df= pd.concat([batch_result_df,knn_result_df, pa_results_df, ht_result_df, hat_result_df, arf_results_df,snarimax_results_df])
    df= pd.concat([batch_result_df,knn_result_df, pa_results_df, ht_result_df, hat_result_df, arf_results_df,snarimax_results_df])
    # df= pd.concat([batch_result_df,knn_result_df, pa_results_df])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    grouped = df.groupby('model')

    plt.clf()

    fig, ax = plt.subplots(figsize=(15, 5))
    metric = 'RMSE'  
    grouped[metric].plot(rot=45, title=metric, legend=True, ax=ax)
    ax.grid(linestyle=':')
    fig.suptitle("RMSE" )
    plt.tight_layout()


    fig, ax = plt.subplots(figsize=(15, 5))
    metric = 'MAE' 
    grouped[metric].plot(rot=45, title=metric, legend=True, ax=ax)
    ax.grid(linestyle=':')
    fig.suptitle("MAE")
    plt.tight_layout()

    fig, ax = plt.subplots(figsize=(15, 5))
    metric = 'SMAPE'  
    grouped[metric].plot(rot=45, title=metric, legend=True, ax=ax)
    ax.grid(linestyle=':')
    fig.suptitle("SMAPE")
    plt.tight_layout()

    plt.show()

    # Sleep for 60 seconds
    sleep(60)

    # Close all figures
    plt.close('all')

