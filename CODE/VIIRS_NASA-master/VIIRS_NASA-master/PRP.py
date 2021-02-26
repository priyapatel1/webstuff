# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:42:08 2020

@author: priya
"""

import os
path = "C:\\Users\\patelp23\\OneDrive - University of Toronto\\nasa\\VIIRS_NASA-master\\VIIRS_NASA-master"
# path = "C:\\Users\\priya\\OneDrive - University of Toronto\\nasa\\VIIRS_NASA-master\\VIIRS_NASA-master"
os.chdir(path)

# pip install netCDF4
import numpy as np
import pandas as pd
import sys
from netCDF4 import Dataset
import matplotlib.pyplot as plt
#Colab requires specific installation of cartopy
#apt-get -qq install python-cartopy python3-cartopy;
#pip uninstall -y shapely;    # cartopy and shapely aren't friends (early 2020)
#pip install shapely --no-binary shapely;
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh
from textwrap import wrap

#!/usr/bin/python
try:
    fileList = open('fileList.txt', 'r')
except:
    print('Did not find a text file containing file names (perhaps name does not match)')
    sys.exit()

#loops through all files listed in the text file
for FILE_NAME in fileList:
    FILE_NAME=FILE_NAME.strip()
    #change 'raw_input' to 'input' if an error is shown about the input
    user_input=input('\nWould you like to process\n' + FILE_NAME + '\n\n(Y/N)')
    if(user_input == 'N' or user_input == 'n'):
        print('Skipping...')
        continue
    else:
        file = Dataset(FILE_NAME, 'r')
# read the data
        ds=file
        print(ds)
        #grp='PRODUCT'        
        lat= ds.variables['Latitude'][:][:]
        lon= ds.variables['Longitude'][:][:]
        if 'AERDB' in FILE_NAME:
            
            #The user has a choice of 5 sds variable and has to input a number to choose.
            #The loop keeps repeating until the user inputs a value between 1-5 inclusive.
            while  True:
              choice = input("""Pick the number with the corresponding sds variable of your choice: 
              1) Aerosol_Optical_Thickness_550_Land
              2) Aerosol_Optical_Thickness_550_Land_Ocean_Best_Estimate
              3) Aerosol_Optical_Thickness_QA_Flag_Land
              4) Aerosol_Type_Land_Ocean
              5) Angstrom_Exponent_Land_Ocean_Best_Estimate """)
              
              if choice in ['1', '2', '3', '4', '5']:
                break
              else:
                print("Please input a valid response!")


            if choice == '1':
              sds_name='Aerosol_Optical_Thickness_550_Land'
            elif choice =='2':
              sds_name='Aerosol_Optical_Thickness_550_Land_Ocean_Best_Estimate'
            elif choice =='3':
              sds_name='Aerosol_Optical_Thickness_QA_Flag_Land'
            elif choice =='4':
              sds_name='Aerosol_Type_Land_Ocean'
            elif choice =='5':
              sds_name='Angstrom_Exponent_Land_Ocean_Best_Estimate'

        data= ds.variables[sds_name]
        map_label = sds_name
        map_label = map_label.replace('_', ' ')
        map_label = '\n'.join(wrap(map_label, 40)) 
        #get necessary attributes 
        fv=data._FillValue

        #get lat and lon information 
        min_lat=np.min(lat)
        max_lat=np.max(lat)
        min_lon=np.min(lon)
        max_lon=np.max(lon)
        
        # set map labels
        #map_label = data.units
        map_title = data.long_name
        #print(data.units)
    
        #get the data as an array and mask fill/missing values
        dataArray=np.array(data[:][:])
        dataArray = np.multiply(dataArray, 1.0)
        fv = fv*1.0
        dataArray[dataArray==fv]=np.nan
        data=dataArray
        
        
        #get statistics about data
        average=np.nanmean(dataArray)
        stdev=np.nanstd(dataArray)
        median=np.nanmedian(dataArray)
        vmax = np.nanmax(dataArray)
        
        #print statistics 
        print('The average of this data is: ',round(average,3),'\nThe standard deviation is: ',round(stdev,3),'\nThe median is: ',round(median,3))
        print('The range of latitude in this file is: ',min_lat,' to ',max_lat, 'degrees \nThe range of longitude in this file is: ',min_lon, ' to ',max_lon,' degrees')
        #change 'raw_input' to 'input' if an error is shown about the input
        is_map=input('\nWould you like to create a map of this data? Please enter Y or N \n')
        
        #if user would like a map, view it
        if is_map == 'Y' or is_map == 'y':
          ax = plt.axes(projection=ccrs.LambertConformal())
          extent = [min_lon, max_lon, min_lat, max_lat]
          ax.coastlines() #outlines the continents          
          ax.set_extent(extent)
          
          my_cmap = plt.cm.get_cmap('jet')
          my_cmap.set_under('w')
          plt.pcolormesh(lon, lat, data, vmin=0.0, vmax=vmax, cmap=my_cmap, transform=ccrs.PlateCarree())
          plt.autoscale()
          #title the plot
          plt.title('{0}\n {1}'.format(FILE_NAME, map_title))
          fig = plt.gcf()
          cb = plt.colorbar(shrink = 0.7)
          cb.set_label(map_label, fontsize =9, wrap=True)
          """
            grd = m.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
            grd.xlabels_top = None
            grd.ylabels_right = None
            grd.xformatter = LONGITUDE_FORMATTER
            grd.yformatter = LATITUDE_FORMATTER
            """
          # Show the plot window.
          plt.show()
          #once you close the map it asks if you'd like to save it
          #change 'raw_input' to 'input' if an error is shown about the input    
          is_save=str(input('\nWould you like to save this map? Please enter Y or N \n'))
          if is_save == 'Y' or is_save == 'y':
            #saves as a png if the user would like
            pngfile = '{0}.png'.format(FILE_NAME[:-3])
            fig.savefig(pngfile, dpi = 300, bbox_inches='tight')
        #close the hdf5 file 
        file.close()
