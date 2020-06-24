from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource, CustomJS, CustomJSFilter, 
    GeoJSONDataSource, HoverTool, LinearColorMapper, Slider, Title, Legend, DatetimeTickFormatter, Text)
from bokeh.models.ranges import DataRange1d
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure, show, output_notebook, output_file

from jdcv19.gis.gis import ZipCodeGIS
from jdcv19.dataset.cases import SanDiegoCasesByZipCode

import numpy as np
import pandas as pd

def create_map(gis: ZipCodeGIS, colors='gray') -> figure:
    """ One line summary.
    
    Parameters
    ----------
    gis : gis.ZipCodeGIS
    
    colors: DataFrame with zipcode and color
    
    Returns
    ----------
    mapfig  
        a Bokeh Figure showing county subdivisions and zipcode points.  
    
        mapfig.renderers[0].data_source with name="zipcode_coordinates" is datasource of points
    
    """
    geosource = GeoJSONDataSource(geojson=gis.geojson)
    aspect_ratio = np.abs(np.diff(gis.latrange)[0])/np.abs(np.diff(gis.lonrange)[0])

    f = figure(title="San Diego County: Hover to select Zip Code",tools=[],
            plot_width=400,aspect_ratio=aspect_ratio,
            x_axis_label='Longitude',y_axis_label='Latitude')
    f.toolbar.logo = None
    f.toolbar_location = None
    
    subdivisions = f.patches('xs','ys',source = geosource,
                             fill_color = None,
                             line_color = 'gray',
                             line_width = 0.25,
                             fill_alpha = 1)
    
    zipcodes_source = gis.zipcode_coordinates[['city','latitude','longitude']]; 
    
    if isinstance(colors,str):
        zipcodes_source['color'] = colors
    elif isinstance(colors,pd.DataFrame):
        zipcodes_source = zipcodes_source.join(colors,how='inner')
    
    zipcodes_source = ColumnDataSource(zipcodes_source)
    
    
    renderer = f.scatter(source=zipcodes_source,x='longitude',y='latitude',
                color='color',name='zipcode_point_renderer')
                    
    f.add_tools(HoverTool(renderers = [renderer],
                          tooltips = [('Zip Code:','@zip'),('City:','@city')]))
                          
    return f
        

def create_timeseries(df: pd.DataFrame) -> figure:
    """ One line summary.
 
    Parameters
    ----------
    df : Pandas DataFrame TimeSeries.  Index is Dates in Time Series.
 
    Returns
    ----------
    tsfid
 
    """
    y_range = DataRange1d(bounds=df.ts.value_range)
    x_range = DataRange1d(bounds=df.ts.date_range)
    
    f = figure(plot_width=800,tools=[],plot_height=500,x_range=x_range,y_range=y_range,
            x_axis_type='datetime',y_axis_label='Total Reported Cases',x_axis_label='Date',
            title='Total Reported Cases in Selected Zip Code by Date')
    f.xaxis.major_label_overrides = df.ts.dates_dict
    f.xaxis.major_label_orientation = .75
    f.toolbar.logo = None
    f.toolbar_location = None
           
           
    #ys=casedata.by_zip_array
    #xs = len(ys)*[casedata.day_range.values]
    ys = df.ts.value_array
    xs = df.ts.dates_array
    
    graylines = f.multi_line(xs,ys, line_color='#e5e7f1')
    
    # Create highlight renderer
    highlight_datasource = ColumnDataSource({'Day':[],'Cases':[]})
    f.line(source=highlight_datasource, x='Day',y='Cases',color="#3a41d8",line_width=10,name='highlighted_zipcode_line_renderer')
    f.circle(source=highlight_datasource, x='Day',y='Cases',size=14,color="#3a41d8") 
        
    return f

def link_map_and_timeseries(mapfig: figure,tsfig: figure, datadict: dict) -> (figure,figure):
        
    code = """
    const cases_by_zipcode = %s
    console.log(cases_by_zipcode)
    const index = cb_data.index.indices[0]
    const zipcode = map_source.data.zip[index]
    console.log(zipcode)
    console.log(cases_by_zipcode[zipcode])
    console.log(cases_by_zipcode['Day'])
    const data = {'Day':cases_timeseries.data['Day'],'Cases':cases_timeseries.data['Cases']}
    if (typeof cases_by_zipcode[zipcode] !== 'undefined') {
        data['Cases'] = Object.values(cases_by_zipcode[zipcode])
        data['Day'] = Object.values(cases_by_zipcode['Day'])
    } 
    cases_timeseries.data = data
    """ % datadict
    

    zipcodes_datasource = mapfig.select(name='zipcode_point_renderer').data_source
    timeseries_datasource = tsfig.select(name='highlighted_zipcode_line_renderer').data_source
    callback = CustomJS(args={'map_source': zipcodes_datasource, 'cases_timeseries':timeseries_datasource}, code=code)
    mapfig.add_tools(HoverTool(tooltips=None, callback=callback, renderers=mapfig.select(name='zipcode_point_renderer')))
    return mapfig, tsfig
