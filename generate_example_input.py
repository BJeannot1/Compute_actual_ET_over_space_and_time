import netCDF4
import numpy as np
from Utilities import *

#read data
#Reading and processing time data
Date0=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",nbr_lignes_header=1,separator=";"),0),str)

#reading other data
Patm=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),1),float)

HR=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),2),float)

RG=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),3),float)

Temp=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),4),float)

Vent10m=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),5),float)

Pbrute=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),6),float)

foo=np.array(column(Personal_file_read_function(path="Input/localisation_site.csv",
    nbr_lignes_header=0,nbr_lignes_a_lire=0,
    separator=";"),1),float)
lat_deg=foo[0]
lm=foo[1] # Longitude du site de mesure (degrées O par rapport au Greenwich
lz=foo[2] # Lz longitude of the center of the local time zone

Rfumax=np.loadtxt("Input/rfumax.txt",skiprows=1) 
Kc=np.loadtxt("Input/crop_coef.txt",skiprows=1) # Taking into account the crop coefficient


#create empty test netcdf file
rootgrp=netCDF4.Dataset('Input.nc',"w",format="NETCDF4")
#create dimensions
time=rootgrp.createDimension("time", None)
lat=rootgrp.createDimension("lat", 10)
lon=rootgrp.createDimension("lon", 10)
#create non-time-dependent variables
times=rootgrp.createVariable("time","str",("time",)) 
times.unit="time in %d/%m/%Y %H:%M"
latitudes=rootgrp.createVariable("lat","f4",("lat",)) 
latitudes.unit="°N"
longitudes=rootgrp.createVariable("lon","f4",("lon",))
longitudes.unit="°O"
lons_centre_tz=rootgrp.createVariable("lon_ct_tz","f4",("lon",))
lons_centre_tz.unit="°O"
#create time-dependent variables
temp=rootgrp.createVariable("temp","f4",("time","lat","lon",))
temp.unit="°C"
patm=rootgrp.createVariable("patm","f4",("time","lat","lon",))
patm.unit="hPa"
hr=rootgrp.createVariable("hr","f4",("time","lat","lon",))
hr.unit="%"
v10m=rootgrp.createVariable("v10m","f4",("time","lat","lon",))
v10m.unit="m/s"
pbr=rootgrp.createVariable("pbr","f4",("time","lat","lon",))
pbr.unit="mm/h"
rg=rootgrp.createVariable("rg","f4",("time","lat","lon",))
rg.unit="Joules/cm²"
rfumax=rootgrp.createVariable("rfumax","f4",("time","lat","lon",))
rfumax.unit="mm"
kc=rootgrp.createVariable("kc","f4",("lat","lon",))
kc.unit="-"
#writing data
lons =  np.arange(356.8,357.8,0.1)
lats =  np.arange(46.0,47.0,0.1)
lons_ctre_tz =  np.full((len(lons)),357.3)
latitudes[:]=lats
longitudes[:]=lons
lons_centre_tz[:]=lons_ctre_tz
times[:]=Date0

nlats = len(rootgrp.dimensions["lat"])
nlons = len(rootgrp.dimensions["lon"])
for i in range(nlats):
    for j in range (nlons):
        temp[:, i, j]= Temp+0.5*i
        patm[:, i, j]= Patm
        hr[:, i, j]= HR
        v10m[:, i, j]= Vent10m+0.2*j
        pbr[:, i, j]= Pbrute
        rg[:, i, j]= RG
rfumax[:,:,:]=np.full((len(Date0),nlats,nlons),Rfumax)
kc[:,:]=np.full((nlats,nlons),Kc)       
rootgrp.close()
