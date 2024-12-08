import pandas as pd

def create_city_mapping():
    df = pd.read_csv("locality_id.csv", skiprows=1)
    df.reset_index(inplace=True)
    rows_drop = []
    for i in range(0, len(df)):
        cityname = df.iloc[i]["cityName"]
        if(cityname == "Live Weather - A Zomato Giveback\rThe list of cities and localities where live weather information is available" ) or (cityname == "The list of cities and localities where live weather information is available") or (cityname=="Live Weather - A Zomato Giveback") or (cityname == 'cityName'):
            rows_drop.append(i)

    df = df.drop(rows_drop)
    df.reset_index(inplace=True) #All extra lines removed

    cities = df["cityName"].unique() 

    city_loc = {}
    for i in cities:
        city_loc[i] = ""

    for i in range(0, len(df)):
        city = df.iloc[i]["cityName"]
        locality = df.iloc[i]["localityName"]
        city_loc[city] = city_loc[city]  +locality + "|"
    
    return city_loc

#print(city_loc["Kolkata"][:-1])
#print(city_loc["Kolkata"][:-1].split("|"))

def locality_id_mapping():
    df = pd.read_csv("locality_id.csv", skiprows=1)
    df.reset_index(inplace=True)
    locality_id_dic = {}
    for i in range(0, len(df)):
        locality = df.iloc[i]["localityName"]
        id = df.iloc[i]["localityId"]
        locality_id_dic[locality] = id 

    return locality_id_dic
