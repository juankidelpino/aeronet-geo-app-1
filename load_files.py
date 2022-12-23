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

ALWAYS_FETCH_DATA = True #BOOLEAN globally overrides existing data and fetches new sets
RELOAD_FABRIC_DATA = False #BOOLEAN overrides existing fabric coordinate dictionary and generates a new one

def load_files():
    #Get all accounts and services from Sonar
    if not os.path.exists('all_active_accounts.csv') or ALWAYS_FETCH_DATA:
        accounts = sonarcrud.get_all_accounts(True, None)

    else:
        print('Using Saved Accounts...')

    if not os.path.exists('all_services.csv') or ALWAYS_FETCH_DATA:
        services = sonarcrud.get_all_services()

    else:
        print('Using Saved Services...')

    """
    GET ALL SERVICES, CREATE A DICTIONARY TO MAP SERVICE ID TO  SERVICE OBJECT (THEN GET ACCOUNT SERVICES AND USE ID TO MATCH SERVICE DETIALS)
    data_service boolean (12 from 0)
    technology_code (FIBRA) = 50 ELSE no fibra (15 from 0)
    """

    #Creating Dictionary for service information
    services_dict = {}

    for idx, row in enumerate(services):

        service_id = row['id']

        services_dict[service_id] = {'data_service': row['data_service'], 'technology_code': row['technology_code'], 'full_service': row}


    #Creating Dictionary for accounts and relevant service information
    accounts_with_services = {}
            
    #Fetching Account Services for active accounts 

    for idx, row in enumerate(accounts):

        account_id = row['id']
        print('Getting Account services for: ', account_id)
        service_data, pagination = sonarcrud.get_account_services(account_id)

        #Create a dictionary for matching account IDs to corresponding service IDs
        if len(service_data) > 0:

            accounts_with_services[account_id] = []

            for service in service_data:

                service_id = service['id']

                accounts_with_services[account_id].append(service_id)

    #Create a dictionary for the final account-service objects
    accounts_full_service = {}

    #Find valid fiber clients
    for account_id in accounts_with_services.keys():
        
        for service_id in accounts_with_services[account_id]:

            data = services_dict[service_id]

            if data['data_service'] and data['technology_code'] == 50:

                accounts_full_service[account_id] = services_dict[service_id]['full_service']
    


    #Create a GeoDataFrame to hold the final form of the data
    accounts_full_coords = gpd.GeoDataFrame([['01010101', Point(0,0)]], columns=['Account ID', 'geometry'])

    #Add the corresponding sonar coordinates to each account
    if not os.path.exists('accounts_full_coords.pickle') or ALWAYS_FETCH_DATA: ######## Replace the pull accounts flag

        for account_id in accounts_full_service.keys():

            addresses = sonarcrud.fetch_account_addresses(account_id)
            physical_address = {}

            for addy in addresses:

                if addy['address_type_id'] == 1:

                    physical_address = addy

            latitude = physical_address['latitude']
            longitude = physical_address['longitude']
            
            temp_gdf1 = gpd.GeoDataFrame([[str(account_id), Point(float(latitude), float(longitude))]], columns=['Account ID', 'geometry'])

            accounts_full_coords = pd.concat([accounts_full_coords, temp_gdf1], axis=0, join='outer', ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False, sort=False, copy=False)

        accounts_full_coords = accounts_full_coords.iloc[1:,:]

        with open('accounts_full_coords.pickle', 'wb') as acct_pickle:

            pickle.dump(accounts_full_coords, acct_pickle)

    else:

        with open('accounts_full_coords.pickle', 'rb') as acct_pickle:
            print('Loading Pickle 1...')
            accounts_full_coords = pickle.load(acct_pickle)

    #Loading fabric pickles
    with open('fabric_coords.pickle', 'rb') as fab_pickle:

        fabric_coords = pickle.load(fab_pickle)

    # with open('fabric_dictionary.pickle', 'rb') as fabd_pickle:
    #     print('Loading Pickle 2...')
    #     fabric_dictionary = pickle.load(fabd_pickle)

    return(accounts_full_coords, fabric_coords)