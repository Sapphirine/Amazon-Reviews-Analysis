import os
import sys
import pandas as pd
import numpy as np
from joblib import dump,load
import time
from datetime import datetime
from sklearn.preprocessing import StandardScaler

#PATH = os.path.join(os.getcwd(),'Desktop','Data Science Project')
data = pd.read_json(sys.argv[1],lines=True)
print("Data Successfully loaded!")

print("Started Cleaning!")
data = data.drop(columns=['market_id','max_item_price','min_item_price','total_busy_dashers','num_distinct_items','order_protocol','platform','store_id','store_primary_category','total_items'])
indexes = np.array(data[(data['total_onshift_dashers'] == "NA") | (data["estimated_store_to_consumer_driving_duration"] == "NA")].index)
data = data.drop(indexes,axis=0)
data = data.reset_index(drop=True)
data["estimated_store_to_consumer_driving_duration"] = data["estimated_store_to_consumer_driving_duration"].astype(int)
data["total_onshift_dashers"] = data["total_onshift_dashers"].astype(int)
data["total_outstanding_orders"] = data["total_outstanding_orders"].astype(int)
zeros = np.array(data[data["total_onshift_dashers"] == 0].index)
data = data.drop(zeros,axis=0)
data = data.reset_index(drop=True)

def day(string):
    return str(string.date().weekday())

a = "06:00:00"
time_1 = datetime.strptime(a,"%H:%M:%S").time()
b = "12:00:00"
time_2 = datetime.strptime(b,"%H:%M:%S").time()
c = "18:00:00"
time_3 = datetime.strptime(c,"%H:%M:%S").time()
print("Cleaning Status: 50%")
def parts_of_day(string):
    time = string.time()
    if time >= time_1 and time < time_2:
        return str(0)
    elif time >= time_2 and time < time_3:
        return str(1)
    elif time >= time_3 or time <= time_1:
        return str(2)

data['Time'] = data['created_at'].apply(parts_of_day)
data['Weekday'] = data['created_at'].apply(day)
data = data.drop(columns=['created_at'])
data['workload'] = data['total_outstanding_orders']/data['total_onshift_dashers']
data = data.drop(columns=["total_onshift_dashers","total_outstanding_orders"])
final_df = data[["delivery_id","estimated_order_place_duration","estimated_store_to_consumer_driving_duration"]]
data = data.drop(columns=["delivery_id","estimated_order_place_duration","estimated_store_to_consumer_driving_duration"])
predict_data = pd.get_dummies(data)
predict_data = predict_data[['workload', 'subtotal', 'Time_0', 'Time_1', 'Time_2', 'Weekday_0',
       'Weekday_1', 'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5',
       'Weekday_6']]
X_sample = predict_data[["workload","subtotal"]]
scaler = StandardScaler().fit(X_sample)
X_sample = scaler.transform(X_sample)
predict_data[["workload","subtotal"]] = X_sample
print("Cleaning done!")
print("Loading Model")
model = load("weights.joblib")
predictions = model.predict(predict_data)
final_df['predicted_time'] = predictions
final_df["predicted_delivery_seconds"] = final_df["predicted_time"] + final_df["estimated_order_place_duration"] + final_df["estimated_store_to_consumer_driving_duration"]
final_df = final_df.drop(columns=["estimated_store_to_consumer_driving_duration","estimated_order_place_duration","predicted_time"])
final_df.to_csv("result.tsv",sep="\t",index=False)
print("Finished! Check the Data Science Project Folder")
