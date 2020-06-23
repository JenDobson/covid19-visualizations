import unittest
import os
import subprocess
import re

import sys
sys.path.append('../src')

import jdcv19.dataset.cases as cases
from jdcv19.dataset.zip_accessor import ZipAccessor
import jdcv19.gis.gis as gis
import jdcv19.figures.figures as f

from bokeh.io import show
from bokeh.plotting import output_file, save 
from bokeh.layouts import row
from bokeh.models import CustomJS, HoverTool

import pandas as pd
import types 

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_FILE_PATH = os.path.join(THIS_PATH,"output")
MAP_OUTPUT_FILE = os.path.join(OUTPUT_FILE_PATH,"test_create_map.html")
MAP_TIMESERIES_OUTPUT_FILE = os.path.join(OUTPUT_FILE_PATH,"test_ts_map_callback.html")
MAP_TIMESERIES_DIFF_OUTPUT_FILE = os.path.join(OUTPUT_FILE_PATH,"test_ts_map_diff_callback.html")



'''
ZipCodeGIS constructor takes an object with a "zipcodes" method
'''
class TestPlots(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        subprocess.run(["rm",MAP_OUTPUT_FILE])
        subprocess.run(["rm",MAP_TIMESERIES_OUTPUT_FILE])
        
    def setUp(self):
        self.casedata = cases.SanDiegoCasesByZipCode(os.path.join(THIS_PATH,'data'))
        
        df = pd.read_csv(os.path.join(THIS_PATH,'data','sandiego_data_by_zipcode.csv'))
        
        self.gis = gis.ZipCodeGIS(df.zip.zipcodes)
        self.files_to_view = []
        
    def test_create_map(self):
        a,b = divmod(len(self.gis.zipcode_coordinates.index),3)
        colors = ['red','green','blue']
        # Change the order of index in color_spec
        color_spec = pd.DataFrame(index = self.gis.zipcode_coordinates.index, data={'color':colors*a + colors[:b]}).iloc[::-1]
        fig = f.create_map(self.gis,color_spec)
        output_file(MAP_OUTPUT_FILE)
        save(fig)
        
    def test_can_add_callback_to_map_figure(self):
        mapfig = f.create_map(self.gis)
        tsfig = f.create_timeseries(self.casedata)
        (mapfig, tsfig) = f.link_map_and_timeseries(mapfig,tsfig,self.casedata.by_zip_dict)
        output_file(MAP_TIMESERIES_OUTPUT_FILE)
        save(row(mapfig,tsfig))
        
    def test_can_create_map_and_ts_with_diff_data(self):
        mapfig = f.create_map(self.gis)
        self.casedata.return_type = 'diff'
        tsfig = f.create_timeseries(self.casedata)
        (mapfig, tsfig) = f.link_map_and_timeseries(mapfig,tsfig,self.casedata.by_zip_dict)
        output_file(MAP_TIMESERIES_DIFF_OUTPUT_FILE)
        save(row(mapfig,tsfig))
        
        
    @classmethod    
    def tearDownClass(cls):
        subprocess.run(["open",MAP_OUTPUT_FILE])
        subprocess.run(["open",MAP_TIMESERIES_OUTPUT_FILE])
        subprocess.run(["open",MAP_TIMESERIES_DIFF_OUTPUT_FILE])