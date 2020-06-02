import unittest

import sys
sys.path.append('../src')

import jdcv19.dataset.cases as cases
import jdcv19.gis.gis as gis


import os
import pandas.testing as pdtest
import pandas as pd
import numpy as np
        
THISDIR = os.path.dirname(os.path.abspath(__file__))



class TestCasesByZipCode(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.join(THISDIR, 'data')        
        self.cases = cases.SanDiegoCasesByZipCode(data_dir)
        
    def test_constructor(self):
        pass
        
    def test_properties_and_methods(self):
        self.assertEqual(len(self.cases.zipcodes),96)
        pdtest.assert_index_equal(self.cases.day_range,pd.RangeIndex(0,4,1))
        self.assertEqual(self.cases.zipcode_count_min,0)
        self.assertEqual(self.cases.zipcode_count_max,65)
        self.assertEqual(np.shape(self.cases.by_zip_array),(97,4))    
        self.assertEqual(self.cases.dates_dict,{0:'2020-03-31',1:'2020-04-01',2:'2020-04-02',3:'2020-04-03'})
        self.assertFalse(self.cases.by_zip_df.isnull().any().any())
        self.assertTrue('Day' in self.cases.by_zip_dict)
        
    def test_can_set_return_type_selector(self):
        self.assertListEqual(list(self.cases.by_zip_df.iloc[-1,0:5].values),[1,10,0,28,24])
        self.cases.return_type = 'diff'
        self.assertListEqual(list(self.cases.by_zip_df.iloc[-1,0:5].values),[0,1,0,5,3])
        self.assertFalse(self.cases.by_zip_df.isnull().any().any())
        
class TestGIS(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(THISDIR, 'data')        
        self.cases = cases.SanDiegoCasesByZipCode(data_dir)
        
        self.gis = gis.ZipCodeGIS(self.cases.zipcodes)
    
    def test_constructor(self):
        pass
        
    def test_properties(self):
        self.assertEqual(self.gis.latrange,(32.556264,33.380359))
        self.assertEqual(self.gis.lonrange,(-117.36077,-116.26597))
        self.assertEqual(self.gis.zipcode_coordinates.shape,(93,3))
        
    def test_methods(self):
        pass

        
        
if __name__ == '__main__':
    unittest.main()
    
    
    