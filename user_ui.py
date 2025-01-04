import os
import streamlit as st
import pandas as pd
import sys
import threading
import requests
import http.client
import json
import time
from helper_files import seasonal_decompose, seasonal_decompose_function, forecast_function

conn = http.client.HTTPSConnection("www.weatherunion.com")
api_key = "869354ac94bfd50c787a3c17ad5fd0b5"
headers = {'X-Zomato-Api-Key' : api_key}

from locality_dictionary_data import create_city_mapping, locality_id_mapping

time_series_cities = ["Select City", "Hyderabad", "Delhi NCR", "Kolkata", "Pune"]
analysis_chosen_city = ["Select City"]
selected_locality = "Select a locality"


st.title("Weather Information Explorer")
st.image("vector_app.jpg")
st.header("Get real time personalized weather information")

city_locality_dictionary = create_city_mapping()
city_lists = list(city_locality_dictionary.keys())
selected_city = st.selectbox("Select a City", options=city_lists)
forecast_mode = "Nothing"

def choose_locality_dropdown(selected_city):
    localities = city_locality_dictionary[selected_city]
    locality_list = localities[:-1].split("|")
    return locality_list

def get_weather_data(locality_id):
    #weather_update_service_url = "http://localhost:5001/weather_update"
    request_data = f"/gw/weather/external/v0/get_locality_weather_data?locality_id={locality_id}"
    conn.request("GET", request_data, headers=headers)
    res = conn.getresponse()
    data = res.read()
    response = data.decode("utf-8")
    return response

if selected_city != "Select a city":
    locality_options = choose_locality_dropdown(selected_city)
    locality_options = ["Select a locality"] + locality_options
    selected_locality = st.selectbox("Choose a locality", options=locality_options)

    if selected_locality != "Select a locality":
        #Display results based on selection
        locality_id_dictionary = locality_id_mapping()
        locality_id = locality_id_dictionary[selected_locality]
        result = f"The selected city is '{selected_city}' and its locality '{selected_locality}'"
        st.write(result)
        #st.write(get_weather_data(locality_id))
        weather_info = json.loads(get_weather_data(locality_id))
        weather_df = pd.DataFrame({"Attribute": ["Temperature (°C)","Humidity (%)","Wind Speed (m/s)","Wind Direction (°)","Rain Intensity (mm/hr)","Rain Accumulation (mm)","AQI PM 10","AQI PM 2.5",],
                "Value": [
                    weather_info["locality_weather_data"]["temperature"],
                    weather_info["locality_weather_data"]["humidity"],
                    weather_info["locality_weather_data"]["wind_speed"],
                    weather_info["locality_weather_data"]["wind_direction"],
                    weather_info["locality_weather_data"]["rain_intensity"],
                    weather_info["locality_weather_data"]["rain_accumulation"],
                    weather_info["locality_weather_data"]["aqi_pm_10"] or "Not available",
                    weather_info["locality_weather_data"]["aqi_pm_2_point_5"] or "Not available",],})
        st.table(weather_df)
        st.title("Time Series Analysis")
        analysis_chosen_city = st.selectbox("Select City for Analysis", options=time_series_cities)
        target_variable = "Nothing"
        if analysis_chosen_city != "Select City":
           mode =  st.selectbox("Choose seasonality mode", options=["Multiplicative", "Additive"], index=None)
           target_variable = st.selectbox("Choose target variable for analysis",
                                   options=["Temperature", "Humidity", "Wind Speed"],
                                          index=None)
           if(target_variable != "Nothing"):
               seasonal_decompose_graph = seasonal_decompose_function(analysis_chosen_city, mode, target_variable)
               try:
                   st.subheader("Seasonality - Decomposition Plot")
                   st.pyplot(seasonal_decompose_graph.plot())
                   forecasting = "start"
               except:
                   pass
           st.title("Forecasting Analysis")
           forecast_mode = st.selectbox("Choose forecasting mode", options=["Naive", "ARIMA", "Prophet"])
           if (forecast_mode != "Nothing"):
               forecasting_graph =forecast_function(analysis_chosen_city, forecast_mode, target_variable)
               #print("Forecasting GRAPH TYPE IS ", type(forecasting_graph))
               st.pyplot(forecasting_graph)

