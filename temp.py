import http.client

conn = http.client.HTTPSConnection("www.weatherunion.com")

headers = { 'X-Zomato-Api-Key': "869354ac94bfd50c787a3c17ad5fd0b5" }

conn.request("GET", "/gw/weather/external/v0/get_locality_weather_data?locality_id=ZWL001156", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))