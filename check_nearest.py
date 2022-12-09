import geopandas as gpd
import numpy as np
import pandas as pd

from scipy.spatial import cKDTree
from shapely.geometry import Point

gpd1 = gpd.GeoDataFrame([['John', Point(1, 1)], ['Smith', Point(2, 2)],
                         ['Soap', Point(0, 2)], ['John', Point(0,0)]],
                        columns=['Account ID', 'geometry'])
gpd2 = gpd.GeoDataFrame([['John', Point(0, 1.1)], ['John', Point(2.5, 2)],
                         ['John', Point(1, 1.1)], ['John', Point(0, 1)]],
                        columns=['Location ID', 'geometry'])

def ckdnearest(gdA, gdB):
    # return 0
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    geo_ = nB[idx]
    geo = [Point(x[0],x[1]) for  x in geo_]
    # print('GEO: ', geo)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(geo, name='f_geometry')
            
        ], 
        axis=1)

    return gdf

# ckdnearest(gpd1, gpd2)


