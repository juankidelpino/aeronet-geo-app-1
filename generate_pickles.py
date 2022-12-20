import sonarcrud
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import csv
import os
import pickle
import helpers

#Requires fabric.csv to be present in project folder
#Generates files 'fabric_coords.pickle' and 'fabric_dictionary.pickle'
#Returns tuple ('fabric_dictionary.pickle' , 'fabric_coords.pickle')

#LONG/LAT in FABRIC are index 14-15
#Create a GeoDataFrame for fabric coordinates
fabric_coords = gpd.GeoDataFrame([['01010101', Point(0,0)]], columns=['Location ID', 'geometry'])

def generate_pickles():

    with open("fabric.csv", 'r', encoding="utf8") as f:

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

#Create a dictionary to quickly access coordinates based on location ID
    fabric_dictionary = {}

    fabric_coords.reset_index()

    for index, row in fabric_coords.iterrows():

        fabric_dictionary[row['Location ID']] = {'geometry': row['geometry']}
        
    with open('fabric_dictionary.pickle', 'wb') as handle:

#Dump pickle 2
        pickle.dump(fabric_dictionary, handle)

    return  ( open('fabric_dictionary.pickle', mode='r') , open('fabric_coords.pickle', mode='r') )