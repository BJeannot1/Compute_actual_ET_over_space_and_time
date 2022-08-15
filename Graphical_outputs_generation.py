import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Utilities import *

def Drawmap(NCfile,Time_index,Variable,x,y,t,label_,Title):
    #read input netcdf file
    rootgrp=netCDF4.Dataset('Output.nc',"r",format="NETCDF4")
    latitudes_out=rootgrp.variables[y]
    longitudes_out=rootgrp.variables[x]
    time=rootgrp.variables[t]
    var=rootgrp.variables[Variable]
    # make map
    map = Basemap(projection='merc',llcrnrlon=360-longitudes_out[0],llcrnrlat=latitudes_out[0],urcrnrlon=360-longitudes_out[-1],urcrnrlat=latitudes_out[-1],resolution='i') # projection, lat/lon extents and resolution of polygons to draw
    map.drawcoastlines()
    map.drawstates()
    map.drawcountries()
    map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') 
    map.drawcounties()
    parallels = np.arange(latitudes_out[0],latitudes_out[-1],(-latitudes_out[0]+latitudes_out[-1])/4.01) 
    meridians = np.arange(360-longitudes_out[-1],360-longitudes_out[0],(-longitudes_out[0]+longitudes_out[-1])/4.01) 
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    map.drawlsmask(ocean_color='aqua',lakes=True)
    lons,lats= np.meshgrid(360-longitudes_out[:],latitudes_out[:])
    x,y = map(lons,lats)
    cont = map.contourf(x,y,var[Time_index,:,:])
    cb = map.colorbar(cont,"bottom", size="5%", pad="6%")
    plt.title(Title+ ' at date '+time[Time_index])
    cb.set_label(label_)
    plt.savefig("map_"+str(Time_index))
    plt.close()
    rootgrp.close()


def drawtimeseries(NCfile,latindex,lonindex,t,Variable0,Variable1,lon_,lat_,label_,Title):
    rootgrp=netCDF4.Dataset(NCfile,"r",format="NETCDF4")
    time=rootgrp.variables[t]
    var0=rootgrp.variables[Variable0]
    var1=rootgrp.variables[Variable1]
    longitudes_out=rootgrp.variables[lon_]
    latitudes_out=rootgrp.variables[lat_]
    Date_np=convert_date_str_array_to_NP_object(date_str=time,fmt="%d/%m/%Y %H:%M")
    fig, ax = plt.subplots()
    plt.title(Title+ ' at coords: '+
               "{:.2f}".format(360-longitudes_out[0])+"°E " +
               "{:.2f}".format(latitudes_out[0])+"°N ")
    fig.supylabel(label_,x=-0.0,size=14)
    fig.supxlabel('Date',y=-0.13,size=14)
    y1 =var0[:,latindex,lonindex]
    x1 =Date_np
    ax.plot(x1, y1, label = Variable0,color="black")
    y1 =var1[:,latindex,lonindex]
    x1 =Date_np
    ax.plot(x1, y1, label = Variable1,color="red")
    ax.legend(loc='lower left',bbox_to_anchor=(0.03, 0.8),ncol=1, prop={'size': 12})
    ax.tick_params(axis='x', which='major', labelsize=12)
    ax.tick_params(axis='y', which='major', labelsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(range(1,13,1))))
    ax.xaxis.set_minor_locator(mdates.MonthLocator([1,4,7,10]))
    for label in ax.get_xticklabels(which='major'):label.set(rotation=90)
    plt.savefig("Output_"+Variable0+"_"+Variable1+".png",bbox_inches='tight')
    plt.close()
    rootgrp.close()
