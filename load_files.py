import sonarcrud
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import csv
import os
import pickle
import helpers

ALWAYS_FETCH_DATA = False #BOOLEAN globally overrides existing data and fetches new sets
RELOAD_FABRIC_DATA = False #BOOLEAN overrides existing fabric coordinate dictionary and generates a new one

def load_files():
    if not os.path.exists('all_active_accounts.csv') or ALWAYS_FETCH_DATA:
        accounts = sonarcrud.get_all_accounts(True, None)
        helpers.write_report(accounts, "all_active_accounts.csv")
    else:
        print('Using Saved Accounts...')

    if not os.path.exists('all_services.csv') or ALWAYS_FETCH_DATA:
        services = sonarcrud.get_all_services()
        helpers.write_report(services, "all_services.csv")
    else:
        print('Using Saved Services...')

    """
    GET ALL SERVICES, CREATE A DICTIONARY TO MAP SERVICE ID TO  SERVICE OBJECT (THEN GET ACCOUNT SERVICES AND USE ID TO MATCH SERVICE DETIALS)
    data_service boolean (12 from 0)
    technology_code (FIBRA) = 50 ELSE no fibra (15 from 0)
    """

    #Creating Dictionary for service information
    services_dict = {}

    with open("all_services.csv", 'r') as f:
        reader = csv.reader(f)
        allserv_csv = list(reader)
        for idx, line in enumerate(allserv_csv):
            if idx == 0:
                continue
            service_id = line[0]
            # print('Getting Service ID for: ', service_id)
            services_dict[service_id] = {'data_service': line[12], 'technology_code': line[15], 'full_service': line}
            # print(services_dict[service_id])
        # print(services_dict.keys())

    #Creating Dictionary for account and relevant service information
    accounts_with_services = {}
            
    #Fetching Account Services for active accounts
    if not os.path.exists('accounts_with_services.pickle') or ALWAYS_FETCH_DATA or False:
        with open("all_active_accounts.csv", 'r') as f:
            reader = csv.reader(f)
            allactacc_csv = list(reader)
            for idx, line in enumerate(allactacc_csv):
                if idx == 0:
                    continue
                account_id = line[0]
                print('Getting Account services for: ', account_id)
                service_data, pagination = sonarcrud.get_account_services(account_id)
                
    #Create a dictionary for matching account IDs to corresponding service IDs
                if len(service_data) > 0:
                    accounts_with_services[account_id] = []
                    for service in service_data:
                        service_id = service['id']

                        accounts_with_services[account_id].append(service_id)

        with open('accounts_with_services.pickle', 'wb') as handle:
            pickle.dump(accounts_with_services, handle)
    #Loading pickle data to avoid reorganizing data on every run
    else:
        with open('accounts_with_services.pickle', 'rb') as handle:
            accounts_with_services = pickle.load(handle)

    #Create a dictionary for the final account-service objects
    accounts_full_service = {}

    #Find valid fiber clients
    for account_id in accounts_with_services.keys():
        # print('Account: ', account_id, '  ...  Services: ', accounts_with_services[account_id])
        
        for service_id in accounts_with_services[account_id]:
            # print(services_dict[str(service_id)])
            data = services_dict[str(service_id)]
            # print(data['data_service'], ' --- ', data['technology_code'])
            if data['data_service'] == 'True' and data['technology_code'] == '50':
                accounts_full_service[account_id] = services_dict[str(service_id)]['full_service']
    # print(accounts_full_service)

    #Create a GeoDataFrame to hold the final form of the data
    accounts_full_coords = gpd.GeoDataFrame([['01010101', Point(0,0)]], columns=['Account ID', 'geometry'])

    #Add the corresponding sonar coordinates to each account
    if not os.path.exists('accounts_full_coords.pickle') or ALWAYS_FETCH_DATA:
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
        with open('accounts_full_coords.pickle', 'wb') as handle:
                    pickle.dump(accounts_full_coords, handle)
    else:
        with open('accounts_full_coords.pickle', 'rb') as handle:
            print("Using Saved Account Coordinates...")
            accounts_full_coords = pickle.load(handle)

    print(accounts_full_coords)

    #LONG/LAT in FABRIC are index 14-15
    #Create a GeoDataFrame for fabric coordinates
    fabric_coords = gpd.GeoDataFrame([['01010101', Point(0,0)]], columns=['Location ID', 'geometry'])

    if not os.path.exists('fabric_coords.pickle') or RELOAD_FABRIC_DATA:
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
        print(fabric_coords)
        with open('fabric_coords.pickle', 'wb') as handle:
            pickle.dump(fabric_coords, handle)
    #Loading pickle data (COORDS)
    else:
        with open('fabric_coords.pickle', 'rb') as handle:
            print("Using Saved Fabric Coordinates...")
            fabric_coords = pickle.load(handle)
            # print(fabric_coords)
    #Create a dictionary to quickly access coordinates based on location ID
    fabric_dictionary = {}

    if not os.path.exists('fabric_dictionary.pickle'):
        fabric_coords.reset_index()
        for index, row in fabric_coords.iterrows():
            fabric_dictionary[row['Location ID']] = {'geometry': row['geometry']}
            """
            if index == 0 or index == 1:
               print('Row ', index, ': ', row['geometry'])
            """
            
        with open('fabric_dictionary.pickle', 'wb') as handle:
            pickle.dump(fabric_dictionary, handle)
            # print(fabric_coords)
    else:
        with open('fabric_dictionary.pickle', 'rb') as handle:
            fabric_dictionary = pickle.load(handle)

    return(accounts_full_coords, fabric_coords, fabric_dictionary)