from cgi import test
import math
import sonarcrud
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import csv
import os
import pickle
import helpers
import load_files
import check_nearest
import random
import coms

def runcheck(USE_DEV_ACCOUNTS, USE_DEV_FABRIC):
    files = load_files.load_files()
    # print(files)
    accounts_full_coords, fabric_coords = files 

    # accounts_full_coords = accounts_full_coords.reset_index(inplace=True, drop=True)
    # fabric_coords = fabric_coords.reset_index(inplace=True, drop=True)


    testing_accounts = gpd.GeoDataFrame([['01010101', Point(0,0)]], columns=['Account ID', 'geometry'])
    testing_fabric = gpd.GeoDataFrame([['11010101', Point(0,0)]], columns=['Location ID', 'geometry'])

    if USE_DEV_ACCOUNTS:
        for x in range(20000):
            lat = random.uniform(17.9, 18.4)
            long = random.uniform(-67.1, -65.6)

            temp_testing_accounts = gpd.GeoDataFrame([[str(x), Point(float(lat), float(long))]], columns=['Account ID', 'geometry'])
            testing_accounts = pd.concat([testing_accounts, temp_testing_accounts], axis=0, join='outer', ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False, sort=False, copy=False)

        testing_accounts = testing_accounts.iloc[1:,:]
        testing_accounts = testing_accounts.reset_index(drop=True)
        
        print('Testing Accounts: \n', testing_accounts)
        # testing_accounts.to_csv('C:/Users/Juanki/OneDrive/Work/JP-APPS/aeronet-geo-app/testing_accounts.csv')

    if USE_DEV_FABRIC:
        for x in range(4):
            lat = random.uniform(15, 19)
            long = random.uniform(-60, -67)

            temp_testing_fabric = gpd.GeoDataFrame([[str(x), Point(float(lat), float(long))]], columns=['Location ID', 'geometry'])
            testing_fabric = pd.concat([testing_fabric, temp_testing_fabric], axis=0, join='outer', ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False, sort=False, copy=False)

        testing_fabric = testing_fabric.iloc[1:,:]
        testing_fabric = testing_fabric.reset_index(drop=True)
        print('Testing Accounts to use: ', testing_fabric)

    if USE_DEV_FABRIC and not USE_DEV_ACCOUNTS:
        final_object = check_nearest.ckdnearest(testing_accounts, testing_fabric)
        print(final_object)
    if not USE_DEV_FABRIC and USE_DEV_ACCOUNTS:
        final_object = check_nearest.ckdnearest(testing_accounts, fabric_coords)

        print(final_object)
        
    if USE_DEV_ACCOUNTS and USE_DEV_FABRIC:
        final_object = check_nearest.ckdnearest(testing_accounts, testing_fabric)
        print(final_object)
    if not USE_DEV_FABRIC and not USE_DEV_ACCOUNTS:
        final_object = check_nearest.ckdnearest(accounts_full_coords, fabric_coords)
        print(final_object)

        

    return final_object