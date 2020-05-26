import unittest
import os
import subprocess

import jdcv19.dataset.cases as cases
import jdcv19.gis.gis as gis
import jdcv19.figures.figures as f

from bokeh.io import show
from bokeh.plotting import output_file, save 
from bokeh.layouts import row
from bokeh.models import CustomJS, HoverTool

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_FILE_PATH = os.path.join(THIS_PATH,"output")
MAP_OUTPUT_FILE = os.path.join(OUTPUT_FILE_PATH,"test_create_map.html")
MAP_TIMESERIES_OUTPUT_FILE = os.path.join(OUTPUT_FILE_PATH,"test_ts_map_callback.html")
MAP_TIMESERIES_DIFF_OUTPUT_FILE = os.path.join(OUTPUT_FILE_PATH,"test_ts_map_diff_callback.html")

class TestPlots(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        subprocess.run(["rm",MAP_OUTPUT_FILE])
        subprocess.run(["rm",MAP_TIMESERIES_OUTPUT_FILE])
        
    def setUp(self):
        self.casedata = cases.SanDiegoCasesByZipCode()
        self.gis = gis.ZipCodeGIS(self.casedata.zipcodes)
        self.files_to_view = []
        
    def test_create_map(self):
        
        
        fig = f.create_map(self.gis)
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