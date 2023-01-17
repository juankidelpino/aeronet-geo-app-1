import coms
import runcheck
import flask
import pandas as pd
import geopandas as gpd
import numpy as np
import pickle
import csv
from shapely.geometry import Point



# MAIN -> RUNCHECK -> LOAD_FILES -> RUNCHECK -> MAIN(final_object)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)

USE_DEV_ACCOUNTS = False
USE_DEV_FABRIC = False

def gitcheck_full():
    
    # test = coms.git_test()
    test = coms.reset_git_test()
    who = flask.request.args.get("who", "World")

    return f"Hello {who}!\n"

@app.get("/")
def update_accounts():
    final_object = runcheck.runcheck(USE_DEV_ACCOUNTS, USE_DEV_FABRIC)
    
    final_object = finalize_object(final_object)
    
    result = coms.upload_results(final_object)
    
    return result

def generate_pickles():
    pickle = generate_pickles.generate_pickles()

    return("Pickle Generated Successfuly")

def finalize_object(data):
    
    data["provider_id"] = 370151
    data["brand_name"] = "Aeronet Wireless Broadband LLC"
    data["location_id"] = data['Location ID']
    data["technology"] = 50
    data["max_advertised_download_speed"] = 100
    data["max_advertised_upload_speed"] = 25
    data["low_latency"] = 1
    data["business_residential_code"] = "X"
    
    final_data = data
    final_data.drop(columns="Location ID")
    
    return final_data

def generate_pickles():

    #LONG/LAT in FABRIC are index 14-15
    #Create a GeoDataFrame for fabric coordinates
    fabric_coords = gpd.GeoDataFrame([['01010101', Point(0,0)]], columns=['Location ID', 'geometry'])

    fabric_coords.reset_index()

    with open("FCC_Active_BSL_12312022_ver1.csv", 'r', encoding="utf8") as f:

        reader = csv.reader(f)
        fabric_csv = list(reader)

        for idx, line in enumerate(fabric_csv):

            if idx == 0:
                continue
            location_id = line[0]
            fabric_lat = line[14]
            fabric_long = line[15]

            temp_gdf = gpd.GeoDataFrame([[str(location_id), Point(float(fabric_lat), float(fabric_long))]], columns=['Location ID', 'geometry'])

            fabric_coords = pd.concat([fabric_coords, temp_gdf], axis=0, join='outer', ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False, sort=False, copy=False)

    fabric_coords = fabric_coords.iloc[1:,:]
    
    with open('fabric_coords.pickle', 'wb') as handle:

#Dump pickle 1
        pickle.dump(fabric_coords, handle)
    return "Dis Da Pickle"

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)