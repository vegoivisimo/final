import requests
import pandas as pd
import numpy as np
import datetime


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])

def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

def getPayloadData(data):
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])

def getCoreData(data):
    for core in data['cores']:
        if core['core'] != None:
            response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])


def task1_get_data():
    static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
    response = requests.get(static_json_url)
    
  
    if response.status_code == 200:
        print("TASK 1: API request successful with status code:", response.status_code)
        data = pd.json_normalize(response.json())
        
       
        data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
        
       
        BoosterVersion_temp = []
        for rocket_id in data['rocket']:
            if rocket_id:
                response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(rocket_id)).json()
                BoosterVersion_temp.append(response['name'])
            else:
                BoosterVersion_temp.append(None)
        data['BoosterVersion'] = BoosterVersion_temp
        data = data[data['BoosterVersion'] == 'Falcon 9']
        
        
        data = data[data['cores'].map(len) == 1]
        data = data[data['payloads'].map(len) == 1]
        data['cores'] = data['cores'].map(lambda x: x[0])
        data['payloads'] = data['payloads'].map(lambda x: x[0])
        data['date'] = pd.to_datetime(data['date_utc']).dt.date
        data = data[data['date'] <= datetime.date(2020, 11, 13)]
        
        
        print("\nFirst 5 rows of the DataFrame (Falcon 9 only):")
        print(data.head())
        
        return data
    else:
        print("TASK 1: API request failed with status code:", response.status_code)
        return None


def task2_filter_falcon9(data):
    global BoosterVersion, PayloadMass, Orbit, LaunchSite, Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial, Longitude, Latitude
    
   
    BoosterVersion = []
    PayloadMass = []
    Orbit = []
    LaunchSite = []
    Outcome = []
    Flights = []
    GridFins = []
    Reused = []
    Legs = []
    LandingPad = []
    Block = []
    ReusedCount = []
    Serial = []
    Longitude = []
    Latitude = []
    
    
    getBoosterVersion(data)
    getLaunchSite(data)
    getPayloadData(data)
    getCoreData(data)
    
   
    launch_dict = {
        'FlightNumber': list(data['flight_number']),
        'Date': list(data['date']),
        'BoosterVersion': BoosterVersion,
        'PayloadMass': PayloadMass,
        'Orbit': Orbit,
        'LaunchSite': LaunchSite,
        'Outcome': Outcome,
        'Flights': Flights,
        'GridFins': GridFins,
        'Reused': Reused,
        'Legs': Legs,
        'LandingPad': LandingPad,
        'Block': Block,
        'ReusedCount': ReusedCount,
        'Serial': Serial,
        'Longitude': Longitude,
        'Latitude': Latitude
    }
    
   
    data_falcon9 = pd.DataFrame(launch_dict)
    
   
    data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))
    
    print("\nTASK 2: Processed Falcon 9 launches")
    print("Number of Falcon 9 launches:", data_falcon9.shape[0])
    print("\nFirst 5 rows of Falcon 9 DataFrame:")
    print(data_falcon9.head())
    
    return data_falcon9


def task3_handle_missing_values(data_falcon9):
   
    payload_mass_mean = data_falcon9['PayloadMass'].mean()
    
    
    data_falcon9.loc[:, 'PayloadMass'] = data_falcon9['PayloadMass'].replace(np.nan, payload_mass_mean)
    
   
    print("\nTASK 3: Missing values after handling")
    print(data_falcon9.isnull().sum())
    
   
    data_falcon9.to_csv('dataset_part_1.csv', index=False)
    print("\nData exported to 'dataset_part_1.csv'")
    
    return data_falcon9


if __name__ == "__main__":
    print("=== Starting TASK 1 ===")
    data = task1_get_data()
    
    if data is not None:
        print("\n=== Starting TASK 2 ===")
        data_falcon9 = task2_filter_falcon9(data)
        
        print("\n=== Starting TASK 3 ===")
        final_data = task3_handle_missing_values(data_falcon9)
        
        print("\nFinal DataFrame summary:")
        print(final_data.info())