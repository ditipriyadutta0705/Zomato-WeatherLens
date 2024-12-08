import http.client
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/weather_update', methods=['POST', 'GET'])
def receive_data():
    data = request.get_json() #request.get_json() is a keyword to get data into the function when called or requested
    #print(data)
    conn = http.client.HTTPSConnection("www.weatherunion.com")
    api_key = "869354ac94bfd50c787a3c17ad5fd0b5" #Enter your API key from https://www.weatherunion.com/

    headers = {'X-Zomato-Api-Key' : api_key}
    #print(headers)
    #headers = { 'X-Zomato-Api-Key': "869354ac94bfd50c787a3c17ad5fd0b5" }

    locality_id = data
    request_data = f"/gw/weather/external/v0/get_locality_weather_data?locality_id={locality_id}"
    conn.request("GET", request_data, headers=headers)

    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8"))
    return data.decode("utf-8")


if __name__ == '__main__': #Inuilt python syntax -> like void main() in C 
    app.run(port=5001, debug=True)
    