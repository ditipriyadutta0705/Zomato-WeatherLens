import pandas as pd
import matplotlib.pyplot as plt
from Demos.win32cred_demo import target
from statsmodels.tsa.seasonal import seasonal_decompose

city_dic = {"Hyderabad" : "weather_data/BanjaraHills_6M.csv",
            "Delhi NCR" : "weather_data/KarolBagh_6M.csv",
            "Kolkata" : "weather_data/SaltLake1_6M.csv",
            "Pune" : "weather_data/SadashivPeth_6M.csv"}

feature_dic = {"Temperature":"temperature",
               "Wind Speed":"wind_speed",
               "Humidity":"humidity"}
def seasonal_decompose_function(city, mode, target_variable):
    if(mode == None or target_variable == None):
        return plt.figure(), plt.figure()
    target_variable = feature_dic[target_variable]
    csv_path = city_dic[city]
    df = pd.read_csv(csv_path)
    df["date"] = df["device_date_time"]
    df['date'] = pd.to_datetime(df['date'])
    df = df[["date", target_variable]]
    df.set_index('date', inplace=True)
    df = df.resample("D").mean()
    df[target_variable].fillna(method='ffill', inplace=True)
    df.sort_index(inplace=True)
    result = seasonal_decompose(df[target_variable], model=mode, period=30)
    return result