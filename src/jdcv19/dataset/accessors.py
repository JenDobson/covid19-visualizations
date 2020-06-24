import pandas as pd
import numpy as np
import re

@pd.api.extensions.register_dataframe_accessor("zip")
class ZipAccessor:
    """ Accessor for Cases by Zip Code Data.
    
      
    """
        
    def __init__(self,pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj
        
    @staticmethod
    def _validate(obj):
        # Verify there is at least one zipcode column
        if not obj.columns.map(lambda y: bool(re.match(r'\d{5}',y))).any():
            raise AttributeError("Must have column(s) labeled with 5-digit zipcode")
            
    @property
    def zipcodes(self):
        return self._obj.columns[self._obj.columns.map(lambda y: bool(re.match(r'\d{5}',y)))]
        
@pd.api.extensions.register_dataframe_accessor("ts")
class TSAccessor:
    """ Accessor for TimeSeries DataFrames"""
    
    def __init__(self,pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj
    
    @staticmethod
    def _validate(obj):
        # Verify the index can be a datetime
        pd.to_datetime(obj.index)
        # Verify all values are numbers
        if not obj.applymap(np.isreal).all().all():
            raise ValueError("DataFrame must be numeric")
        
    @property
    def date_range(self):
        return (self._obj.index.min(),self._obj.index.max())
    
    @property
    def value_range(self):
        return (self._obj.min().min(),self._obj.max().max())
    
    @property    
    def dates_dict(self):
        return dict(zip(range(0,len(self._obj.index)),self._obj.index))
    
    @property
    def value_dict(self):
        #d = {x : self._obj[x].values for x in self._obj.columns}
        #return d
        d = {x: dict(zip(range(0,len(self._obj[x].values)),self._obj[x].fillna(0).values)) for x in self._obj.columns}
        return d
    
    @property
    def value_array(self):
        return [np.array(y) for y in self._obj.transpose().to_numpy()]
    
    @property
    def dates_array(self):
        return [np.array(x) for x in np.tile(np.arange(0,len(self._obj)),(len(self._obj.columns),1))]
        
    