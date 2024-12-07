from flask import Flask, request, jsonify
import requests


data = "ZWL003315"

weather_update_service_url = "http://127.0.0.1:5001/weather_update"
response = requests.post(weather_update_service_url, json=data)