#THIS CODE CALCULATES HOURLY ACTUAL EVAPORATION AND HOURLY ACTUAL RECHARGE
#Data needed, in netcdf format :
#-Atmospheric pressure
#-Relative humidity
#-Solar radiation (also called global radiation)
#-Average hourly temperature
#-Wind at 10m
#-Site location
#-Total rain
#-Crop coefficient (i.e. as defined in FAO irrigation and drainage report 56 )
#-easily available water for transpiration (noted RFUMAX, expressed in mm) 

from Utilities import *
from Graphical_outputs_generation import *
import numpy as np
from datetime import datetime
import time
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#read input netcdf file
rootgrp=netCDF4.Dataset('Input.nc',"r",format="NETCDF4")
time=rootgrp.variables["time"]
ntemps=time.shape[0]
lat_deg=rootgrp.variables["lat"]
ny=lat_deg.shape[0]
lon_deg=rootgrp.variables["lon"]
nx=lon_deg.shape[0]
lon_ct_tz=rootgrp.variables["lon_ct_tz"]
temp=rootgrp.variables["temp"]
rg=rootgrp.variables["rg"]
hr=rootgrp.variables["hr"]
pbr=rootgrp.variables["pbr"]
v10m=rootgrp.variables["v10m"]
patm=rootgrp.variables["patm"]
RFUMAX=rootgrp.variables["rfumax"]
KC=rootgrp.variables["kc"]

#create empty output netcdf file
rootgrp_out=netCDF4.Dataset('Output.nc',"w",format="NETCDF4")
    #create dimensions
time_out=rootgrp_out.createDimension("time", ntemps)
lat_out=rootgrp_out.createDimension("lat", ny)
lon_out=rootgrp_out.createDimension("lon", nx)
    #create non-time-dependent variables
times_out=rootgrp_out.createVariable("time","str",("time",)) 
times_out.unit="time in %d/%m/%Y %H:%M"
latitudes_out=rootgrp_out.createVariable("lat","f4",("lat",)) 
latitudes_out.unit="°N"
longitudes_out=rootgrp_out.createVariable("lon","f4",("lon",))
longitudes_out.unit="°O"
    #create time-dependent variables
ETPpot=rootgrp_out.createVariable("Potential ET","f4",("time","lat","lon",))
ETPpot.unit="mm/h"
ETA=rootgrp_out.createVariable("Actual ET","f4",("time","lat","lon",))
ETA.unit="mm/h"
pbr_o=rootgrp_out.createVariable("Total rain","f4",("time","lat","lon",))
pbr_o.unit="mm/h"
recharge_o=rootgrp_out.createVariable("Recharge","f4",("time","lat","lon",))
recharge_o.unit="mm/h"
print ("**CALCULATION OF REFERENCE EVAPOTRANSPIRATION STARTING**")
#processing time_data
Date_np=convert_date_str_array_to_NP_object(date_str=time,fmt="%d/%m/%Y %H:%M")
foo=dt_of_numpy_breakdown(Date_np)
day=column(foo,2)
month=column(foo,1)
year=column(foo,0)
days_since_year_debut=[0]*len(Date_np)
Hours_at_middle_period_since_day_debut=[0.0]*len(Date_np)
t0=[0.0]*len(Date_np)
t1=[0.0]*len(Date_np)
for i in range(0,len(Date_np),1):
    firstdayofyear=np.datetime64(str(year[i]), 'D')
    days_since_year_debut[i]=(np.timedelta64(Date_np[i]-firstdayofyear,"D")+1)/np.timedelta64(1, 'D')
    if i < (len(Date_np)-1):
        firsthourofday=np.datetime64(str(year[i])+"-"+("%02d" % (month[i],))+"-"+("%02d" % (day[i],)), 'h')
        t0[i]=Date_np[i+1]-Date_np[i]
        Hours_at_middle_period_since_day_debut[i]=((Date_np[i]+(t0[i])*0.5   -  firsthourofday )/np.timedelta64(1, 'h'))
        t1[i]=t0[i]/np.timedelta64(1, 'h')
    else:
        t0[i]=t0[i-1]
        Hours_at_middle_period_since_day_debut[i]=((Date_np[i]+(t0[i])*0.5   -  firsthourofday )/np.timedelta64(1, 'h'))     
        t1[i]=t0[i]/np.timedelta64(1, 'h')
days_since_year_debut=np.array(days_since_year_debut)
Hours_at_middle_period_since_day_debut=np.array(Hours_at_middle_period_since_day_debut)
t1=np.array(t1)

#Following FAO56 paper
ET0_mmparh=np.full((ntemps,ny,nx),0.0)
for ilat in range(ny):
    for ilon in range(nx):
        Vent2m=v10m[:,ilat,ilon]*(4.87/(np.log(67.8*10-5.42)))
        gamma=(0.001013*(patm[:,ilat,ilon]/10))/(0.622*2.45) # γ Psychrometric constant (KPa/°C-1)
        e0=0.6108*np.exp((17.27*temp[:,ilat,ilon])/(temp[:,ilat,ilon]+237.3)) #  saturation vapour pressure at the air temperature (Kpa)
        ea=e0*(hr[:,ilat,ilon]/100) # actual vapour pressure (Kpa)
        Triangle=((4098*ea)/(temp[:,ilat,ilon]+237.3)**2) #  slope of saturation vapour pressure curveat air temp (kPa/°C)
        dr=1+0.033*np.cos(((2*np.pi)/365)*days_since_year_debut) # inverse relative distance earth-sun
        delta =0.409*np.sin(((2*np.pi)/365)*days_since_year_debut-1.39) # δ solar declination (rad)
        lat_rad=lat_deg[ilat]*(np.pi/180)
        ws=np.arccos(-np.tan(lat_rad)*np.tan(delta)) # Sunset hour angle
        N=(24/np.pi)*ws
        b=(2*np.pi*(days_since_year_debut-81))/364
        Sc=0.1645*np.sin(2*b)-0.1255*np.cos(b)-0.025*np.sin(b) #Seasonal correction for solar time
        w=(np.pi/12)*((Hours_at_middle_period_since_day_debut+0.06667*(lon_ct_tz[ilon]-lon_deg[ilon])+Sc)-12) #solar time angle at midpoint of the period
        w1=w-((np.pi*t1)/24)
        w2=w+((np.pi*t1)/24)
        Ra=((12*60)/np.pi)*(0.082)*dr*((w2-w1)*np.sin(lat_rad)*np.sin(delta)+np.cos(lat_rad)*np.cos(delta)*(np.sin(w2)-np.sin(w1))) #rayonnement extraterrestre (MJ/m²/h)
        RG_MJparm2parh=rg[:,ilat,ilon]/100.0
        Rso=(0.75+0.00002*500)*Ra # clear-sky solar radiation à partir de Rg (MJ/m²/h)
        Rns=(1-0.23)*RG_MJparm2parh #Net solar radiation à partir de Rg (MJ/m²/h)
        Rnl=0.0000000002043*(((temp[:,ilat,ilon])**4)/2)*(0.34-0.14*np.sqrt(ea))*(1.35*(RG_MJparm2parh/Rso)-0.35) #Net outgoing longwave radiation (MJ/m²/h)
        Rn=Rns-Rnl #Net radiation at the grass surface à partir de Rg (MJ/m²/h)
        Gjour=0.1*Rn
        Gnuit=0.5*Rn
        G=[-999999999.9]*len(RG_MJparm2parh)
        for i in range(0,len(RG_MJparm2parh),1):
            if (RG_MJparm2parh[i]==0.0):
                G[i]=Gnuit[i]
            else:
                G[i]=Gjour[i]
        G=np.array(G)
        ET0_mmparh[:,ilat,ilon]=((0.408*Triangle*(Rn-G)+gamma*(37/(temp[:,ilat,ilon]+273))*Vent2m*(e0-ea))/(Triangle+gamma*(1+0.34*Vent2m)))
print ("**CALCULATION OF REFERENCE EVAPOTRANSPIRATION SUCCESSFUL**")
print ("**CALCULATION OF ACTUAL EVAPOTRANSPIRATION STARTING**")
Recharge=np.full((ntemps,ny,nx),0.0)
ETR=np.full((ntemps,ny,nx),0.0)
for ilat in range(ny):
 for ilon in range(nx):
    #reading and preprocessing of parameters
    Total_rain=pbr[:,ilat,ilon]
    ET0=ET0_mmparh[:,ilat,ilon]
    rfumax=RFUMAX[:,ilat,ilon]
    Kc=KC[ilat,ilon]
    ET0=ET0*Kc
    #CALCULATION OF RECHARGE BY THE METHOD FROM DOURADO & NETO
    Total_rain_minus_ruis=Total_rain #Assumption=no ruisseling
    Pb_minus_ruiss_minus_ETP=Total_rain_minus_ruis-ET0
    RFU=np.array([0.0]*len(Pb_minus_ruiss_minus_ETP))
    APWL=np.array([0.0]*len(Pb_minus_ruiss_minus_ETP))
    RFU[0]=rfumax[0]
    APWL[0]=0.0

    for i in range(1,len(Pb_minus_ruiss_minus_ETP),1):
    #APWL
        if (Pb_minus_ruiss_minus_ETP[i]>0):
            if (RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]>rfumax[i]):
                APWL[i]=0.0
            else:
                APWL[i]=-rfumax[i]*np.log((RFU[i-1]+Pb_minus_ruiss_minus_ETP[i])/rfumax[i])
        else:
            APWL[i]=APWL[i-1]-Pb_minus_ruiss_minus_ETP[i]

    #RFU
        if  (Pb_minus_ruiss_minus_ETP[i]>0):
            if(RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]>rfumax[i]):
                expr1=rfumax[i]
            else:
                expr1=RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]
        else:
            expr1=rfumax[i]*np.exp(-(APWL[i]/rfumax[i]))
            
        if (expr1<0):
                RFU[i]=0.0
        else:
                RFU[i]=expr1

    #RECHARGE
        if(Pb_minus_ruiss_minus_ETP[i]>0):
            ETR[i,ilat,ilon]=ET0[i]
            if(RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]>rfumax[i]):
                     Recharge[i,ilat,ilon]=Pb_minus_ruiss_minus_ETP[i]-(RFU[i]-RFU[i-1])
            else:
                Recharge[i,ilat,ilon]=0.0
        else:
            ETR[i,ilat,ilon]=Total_rain_minus_ruis[i]-(RFU[i]-RFU[i-1])
            Recharge[i,ilat,ilon]=0.0
print ("**CALCULATION OF ACTUAL EVAPOTRANSPIRATION ENDING**")
print ("**OUTPUT NETCDF WRITING**")
#fill output netcdf
recharge_o[:,:,:]=Recharge
ETA[:,:,:]=ETR
pbr_o[:,:,:]=pbr[:,:,:]
ETPpot[:,:,:]=ET0_mmparh
times_out[:]=time[:] 
latitudes_out[:]=lat_deg[:]
longitudes_out[:]=lon_deg[:]
rootgrp_out.close()
rootgrp.close()

print ("**LAST STEP : DRAWING VISUAL OUTPUTS**")
Drawmap(NCfile="Output.nc",
        Time_index=3500,
        Variable="Actual ET",
        x="lon",
        y="lat",
        t="time",
        label_='Actual evapotranspiration (mm/h)',
        Title='Actual evapotranspiration')

drawtimeseries(NCfile="Output.nc",
        latindex=0,
        lonindex=0,
        t="time",
        Variable0="Potential ET",
        Variable1="Actual ET",lon_="lon",lat_="lat",
        label_='Evapotranspiration (mm/h)',
        Title='Potential and Actual evapotranspiration')

drawtimeseries(NCfile="Output.nc",
        latindex=0,
        lonindex=0,
        t="time",
        Variable0="Total rain",
        Variable1="Recharge",lon_="lon",lat_="lat",
        label_='Intensity (mm/h)',
        Title='Total precipitation and actual recharge')


print ("**SCRIPT SUCCESSFUL**")
