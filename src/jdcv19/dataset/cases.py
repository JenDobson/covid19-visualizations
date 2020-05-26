import pandas as pd
import numpy as np

import os
"""Access data with indexing:
    
importlib.reload(dataset.dataset)
ds = dataset.dataset.ZipCodeDataSet()    

"""
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
    
class CasesByZipCode:
    """ Accessor for Cases by Zip Code Data.
    
      
    """
    DATA_DIRECTORY = "./csv"
        
    def __init__(self,datadir="",filename=""):
        if not datadir:    
            datadir = os.path.join(THIS_PATH, self.DATA_DIRECTORY)
        casesfile = os.path.join(datadir,filename)
        self.add_cases_data(casesfile)
        self.add_diff_data()
        self.return_type = 'cases'
           
    def add_cases_data(self,casesfile):
        cases = pd.read_csv(casesfile)
        cases['TOTAL']=cases['TOTAL'].astype('float')
        cases = cases.fillna(0)
        cases = cases.rename(columns={'Data through': 'Date'})
        cases = cases.drop(['Unknown','Date Retrieved'],axis=1)
        cases['Day']=cases.index
        self.__cases = cases
    
    def add_diff_data(self):
        self.__diff = self.__cases.filter(regex="TOTAL|\d{5}|Day").diff()
        self.__diff = self.__diff.fillna(0)
        self.__diff['Day'] = self.__cases['Day']
                    
    @property 
    def return_type(self):
        """Specify whether to return total cases or differential"""
        return self.return_type
        
    @return_type.setter
    def return_type(self,value):
        if value not in ['cases','diff']:
            raise Exception("'{}' is invalid selection type.".format(value))
        if value == 'cases':
            self.__return_type_selector = '_CasesByZipCode__cases'
        elif value == 'diff':
            self.__return_type_selector = '_CasesByZipCode__diff'
            
    @property
    def dates(self):
        return self.__cases['Date']
                    
    @property
    def zipcodes(self):
        """Return list of zipcodes"""
        return self.__cases.columns[self.__cases.columns.str.contains('\d{5}',regex=True)]
    
    @property
    def day_range(self):
        """Return Pandas RangeIndex of dates"""
        return self.__cases.index
    
    @property
    def zipcode_count_min(self):
        """Return minimum case count over all dataset"""
        cc = self.__cases
        return self.by_zip_df.min().min()
        
    @property
    def zipcode_count_max(self):
        """Return maximum case count in one zipcode over all dataset"""
        return self.by_zip_df.max().max()
    
    @property
    def by_zip_df(self,zipcode='all'):
        """Return Pandas DataFrame of cases in specified zipcode(s).  If no zipcode list given, return cases for all zipcodes."""
        if zipcode=='all':
            return getattr(self,self.__return_type_selector).filter(regex="\d{5}|Day")
        else:
            return getattr(self,self.__return_type_selector)[zipcode]
    
    @property
    def by_zip_dict(self):
        return self.by_zip_df.to_dict()
    
    @property    
    def dates_dict(self):
        return self.dates.to_dict()
        
    @property
    def by_zip_array(self):
        return [np.array(y) for y in np.transpose(self.by_zip_df.values)]
        
class SanDiegoCasesByZipCode(CasesByZipCode):
    """
    Extend CasesByZipCode.  Case data populated with San Diego data.
    """
    
    FILENAME = 'sandiego_data_by_zipcode.csv'
    
    def __init__(self,datadir="",filename=""):
        if not datadir:    
            datadir = os.path.join(THIS_PATH, self.DATA_DIRECTORY)
    
        if not filename:
            filename = os.path.join(datadir, self.FILENAME)
        
        super(SanDiegoCasesByZipCode, self).__init__(datadir=datadir,filename=filename)

