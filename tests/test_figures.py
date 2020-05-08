import unittest
import os

import dataset.cases as cases
import gis.gis as gis
import figures.figures as f

from bokeh.io import show
from bokeh.plotting import output_file, save 
from bokeh.layouts import row
from bokeh.models import CustomJS, HoverTool

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
    
class TestPlots(unittest.TestCase):
    
    def setUp(self):
        self.casedata = cases.SanDiegoCasesByZipCode()
        self.gis = gis.ZipCodeGIS(self.casedata.zipcodes)
        
    def test_create_map(self):
        
        
        fig = f.create_map(self.gis)
        output_file(os.path.join(THIS_PATH,"output/test_create_map.html"))
        save(fig)
        
    def test_can_add_callback_to_map_figure(self):
        mapfig = f.create_map(self.gis)
        tsfig = f.create_timeseries(self.casedata)
        (mapfig, tsfig) = f.link_map_and_timeseries(mapfig,tsfig,self.casedata.by_zip_dict)
        output_file(os.path.join(THIS_PATH,"output/test_can_add_callback_to_map_figure.html"))
        save(row(mapfig,tsfig))
        