import requests
import os
import json
import datetime 
BASEURL = "https://restcountries.com/v3.1"
FILENAME = "country.json"
def load_data():
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME,"r") as f:
        return json.load(f)
    


def save_info(data):
    with open(FILENAME,"w") as f:
        json.dump(data,f,indent=2)
    

def get_info():

    country = input("What info do you need info on ?:")
    url = f"{BASEURL}/name/{country}"
    response = requests.get(url)
    time = datetime.datetime.now().strftime("%d %m %y")
    if response.status_code == 200:
        print("Perfectly healthy connection ")
        data = response.json()
        country_data = data
        print(time)
        print(country_data)

        save_info(data)

    else:
        print("shiii bad network fam")
get_info()