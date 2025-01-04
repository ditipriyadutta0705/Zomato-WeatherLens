import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

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

def forecast_function(city, mode, target_variable):
    if(mode == None or target_variable == None):
        return plt.figure()
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
    original_dates = df.index
    original_values = df[target_variable]
    forecast_horizon = 60  # Number of days for forecast
    last_date = df.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
    if(mode == "Naive"):
        print("Entered Naive prediction")
        naive_forecast = df[target_variable].iloc[-1] #Taking the last observed values
        naive_predictions = [naive_forecast] * forecast_horizon
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(original_dates, original_values, label="Original Data", color="Blue")
        ax.plot(forecast_dates, naive_predictions, label="Naive Forecast", color="orange")
        ax.set_title("Time series Forecasting -- Naive")
        ax.set_xlabel("Date")
        ax.set_ylabel("Values")
        ax.legend()
        ax.grid(True)
        #st.text("Naive Forecast")
        graph = fig
        return graph
    elif(mode == "ARIMA"):
        model = ARIMA(df[target_variable], order=(1,1,1)) #p,d,q
        arima_fit = model.fit()
        arima_predictions = arima_fit.forecast(steps=forecast_horizon)
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(original_dates, original_values, label="Original Data", color="Blue")
        ax.plot(forecast_dates, arima_predictions, label = "ARIMA Forecast", color="Orange", linestyle="--")
        ax.set_title("Time series Forecasting -- ARIMA")
        ax.set_xlabel("Date")
        ax.set_ylabel("Values")
        ax.legend()
        ax.grid(True)
        graph = fig
        return graph
    elif(mode == "Prophet"):
        data = df
        data = data.reset_index()
        data.rename(columns={"date":"ds", target_variable:"y"}, inplace=True)
        model =Prophet()
        model.fit(data)
        future = model.make_future_dataframe(periods=60)
        forecast = model.predict(future)
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(data["ds"], data["y"], label="Observed", color="blue")
        ax.plot(forecast["ds"], forecast["yhat"], color="orange")
        ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="orange", alpha=0.2, label="Confidence Interval")
        ax.set_title("Time series Forecasting -- Prophet")
        ax.set_xlabel("Date")
        ax.set_ylabel("Values")
        ax.legend()
        graph = fig
        return graph