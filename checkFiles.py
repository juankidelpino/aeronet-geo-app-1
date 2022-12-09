import csv
import pandas
import geopandas
import pickle

with open('fabric_coords.pickle', 'rb') as handle:
        fabric_coords = pickle.load(handle)

fabric_coords = fabric_coords.iloc[1:,:]

with open('fabric_coords.pickle', 'wb') as handle:
            pickle.dump(fabric_coords, handle)
print(fabric_coords)


with open('accounts_full_coords.pickle', 'rb') as handle:
        accounts_full_coords = pickle.load(handle)

accounts_full_coords = accounts_full_coords.iloc[1:,:]

with open('accounts_full_coords.pickle', 'wb') as handle:
            pickle.dump(accounts_full_coords, handle)
print(accounts_full_coords)
