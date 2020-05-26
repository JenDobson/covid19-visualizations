import geopandas
import json

import shapely
from shapely.geometry import Polygon

import os


class ZipCodeGIS:
    """ Accessor for San Diego GIS data """

    GIS_DIRECTORY = "./data"

    def __init__(self,zipcodes):
        
        this_path = os.path.abspath(os.path.dirname(__file__))
        
        shapefile = os.path.join(this_path,self.GIS_DIRECTORY,'us-zip-code-latitude-and-longitude.shp')
        subdivisionsfile = os.path.join(this_path,self.GIS_DIRECTORY,'cb_2018_06_cousub_500k/cb_2018_06_cousub_500k.shp')    
        
        gis = geopandas.read_file(shapefile)
        
        if not zipcodes.empty:
            gis = gis[gis['zip'].isin(zipcodes)]
        
        gis.index = gis['zip']

        # Correct 92058 and 92093; data from unitedstateszipcodes.org
        gis.loc[gis[gis['zip']=='92058'].index,['latitude','longitude']] = (33.26, -117.35)
        gis.loc[gis[gis['zip']=='92093'].index,['latitude','longitude']] = (32.88, -117.24)
        
        self.__gis = gis
        self.__subdivisions = geopandas.read_file(subdivisionsfile)
        
        self.__compute_geojson()
        
        
    @property
    def latrange(self):
        return (self.__gis['latitude'].min(),self.__gis['latitude'].max())
    @property
    def lonrange(self):
        return (self.__gis['longitude'].min(),self.__gis['longitude'].max())
    @property
    def geojson(self):
        return self.__geojson
    
    @property
    def zipcode_coordinates(self):
        return self.__gis[['city','latitude','longitude']]
        
    def __compute_geojson(self):
        indices = [(0,0),(0,1),(1,1),(1,0),(0,0)]
        polygon = Polygon([(self.lonrange[x[0]],self.latrange[x[1]]) for x in indices])
        clipped = geopandas.clip(self.__subdivisions,polygon)
        self.__geojson = clipped.to_json()