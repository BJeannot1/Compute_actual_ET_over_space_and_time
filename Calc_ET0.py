#THIS CODE CALCULATES REFERENCE EVAPOTRANSPIRATION AT A HOURLY TIME STEP FROM THE FOLLOWING DATA :
#-Atmospheric pressure
#-Relative humidity
#-Solar radiation (also called global radiation)
#-Average hourly temperature
#-Wind at 10m/s
##The methodology follows the recommandations of the Food and Agriculture iirigation and drainage paper n°56

from Utilities import *
import numpy as np
import time
print ("**CALCULATION OF REFERENCE EVAPOTRANSPIRATION STARTING**")

#Reading and processing time data
Date0=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",nbr_lignes_header=1,separator=";"),0),str)
Date_np=convert_date_str_array_to_NP_object(date_str=Date0,fmt="%d/%m/%Y %H:%M")
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

#Following FAO56 paper
Vent2m=Vent10m*(4.87/(np.log(67.8*10-5.42)))
gamma=(0.001013*(Patm/10))/(0.622*2.45) # γ Psychrometric constant (KPa/°C-1)
e0=0.6108*np.exp((17.27*Temp)/(Temp+237.3)) #  saturation vapour pressure at the air temperature (Kpa)
ea=e0*(HR/100) # actual vapour pressure (Kpa)
Triangle=((4098*ea)/(Temp+237.3)**2) #  slope of saturation vapour pressure curveat air temp (kPa/°C)
dr=1+0.033*np.cos(((2*np.pi)/365)*days_since_year_debut) # inverse relative distance earth-sun
delta =0.409*np.sin(((2*np.pi)/365)*days_since_year_debut-1.39) # δ solar declination (rad)
lat_rad=lat_deg*(np.pi/180)
ws=np.arccos(-np.tan(lat_rad)*np.tan(delta)) # Sunset hour angle
N=(24/np.pi)*ws
b=(2*np.pi*(days_since_year_debut-81))/364
Sc=0.1645*np.sin(2*b)-0.1255*np.cos(b)-0.025*np.sin(b) #Seasonal correction for solar time
w=(np.pi/12)*((Hours_at_middle_period_since_day_debut+0.06667*(lz-lm)+Sc)-12) #solar time angle at midpoint of the period
w1=w-((np.pi*t1)/24)
w2=w+((np.pi*t1)/24)
Ra=((12*60)/np.pi)*(0.082)*dr*((w2-w1)*np.sin(lat_rad)*np.sin(delta)+np.cos(lat_rad)*np.cos(delta)*(np.sin(w2)-np.sin(w1))) #rayonnement extraterrestre (MJ/m²/h)
RG_MJparm2parh=RG/100.0
Rso=(0.75+0.00002*500)*Ra # clear-sky solar radiation à partir de Rg (MJ/m²/h)
Rns=(1-0.23)*RG_MJparm2parh #Net solar radiation à partir de Rg (MJ/m²/h)
Rnl=0.0000000002043*(((Temp)**4)/2)*(0.34-0.14*np.sqrt(ea))*(1.35*(RG_MJparm2parh/Rso)-0.35) #Net outgoing longwave radiation (MJ/m²/h)
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
ET0_mmparh=((0.408*Triangle*(Rn-G)+gamma*(37/(Temp+273))*Vent2m*(e0-ea))/(Triangle+gamma*(1+0.34*Vent2m)))

#OUTPUT WRITING
h=open("Temp/ReferenceEvapotranspiration.csv","w")
nom=[]
nom.append("Date")
nom.append("ET0 (mm/h)")
for i in range(0,len(nom),1):
    if (i< len(nom)-1):
        h.write(str(nom[i])+";")
    else:
        h.write(str(nom[i])+"\n")
        
for i in range(0,len(Date_np),1):
    h.write(str(Date0[i])+";")
    h.write(str(ET0_mmparh[i])+"\n")
h.close()

print ("**CALCULATION OF REFERENCE EVAPOTRANSPIRATION ENDED SUCCESSFULLY**")
time.sleep(1)
