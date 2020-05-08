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
           
    def add_cases_data(self,casesfile):
        cases = pd.read_csv(casesfile)
        cases['TOTAL']=cases['TOTAL'].astype('float')
        cases = cases.fillna(0)
        cases = cases.rename(columns={'Data through': 'Date'})
        cases = cases.drop(['Unknown','Date Retrieved'],axis=1)
        cases['Day']=cases.index
        self.__cases = cases
                
    @property
    def dates(self):
        return self.__cases['Date']
                    
    @property
    def last_day_total_cases(self):
        return self.__cases['Total'].iloc[-1]
    
    @property
    def zipcodes(self):
        return self.__cases.columns[self.__cases.columns.str.contains('\d{5}',regex=True)]
    
    @property
    def day_range(self):
        return self.__cases.index
    
    @property
    def zipcode_count_min(self):
        cc = self.__cases
        return self.by_zip_df.min().min()
        
    @property
    def zipcode_count_max(self):
        return self.by_zip_df.max().max()
    
    @property
    def by_zip_df(self,zipcode='all'):
        if zipcode=='all':
            return self.__cases.filter(regex="\d{5}|Day")
        else:
            return self.__cases[zipcode]
    @property
    def by_zip_dict(self):
        return self.by_zip_df.to_dict()
    
    @property    
    def dates_dict(self):
        return self.dates.to_dict()
        
    def stats(self):
        cc = self.__cases
        import pdb; pdb.set_trace()
    @property
    def by_zip_array(self):
        return [np.array(y) for y in np.transpose(self.by_zip_df.values)]
    
    def timeseries_for_zipcode(self,zipcode):
        return self.by_zip_df[zipcode]
    
    def quartiles(self):
        import pdb; pdb.set_trace()
        final_day_quantiles = zipcode_cases.iloc[-1,:].quantile([.25,.5,.75])
        
class SanDiegoCasesByZipCode(CasesByZipCode):
    
    FILENAME = 'sandiego_data_by_zipcode.csv'
    
    def __init__(self,datadir="",filename=""):
        if not datadir:    
            datadir = os.path.join(THIS_PATH, self.DATA_DIRECTORY)
    
        if not filename:
            filename = os.path.join(datadir, self.FILENAME)
        
        super(SanDiegoCasesByZipCode, self).__init__(datadir=datadir,filename=filename)
  