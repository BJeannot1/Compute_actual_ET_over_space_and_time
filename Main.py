
#THIS CODE CALCULATES HOURLY ACTUAL EVAPORATION AND HOURLY ACTUAL RECHARGE
#Data needed :
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
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Calculating reference evapotranspiration
exec(open("Calc_ET0.py").read())
print("**CALCULATION OF ACTUAL EVAPOTRANSPIRATION AND RECHARGE**")
#reading and preprocessing of parameters
Date0=np.array(column(Personal_file_read_function(path="Temp/ReferenceEvapotranspiration.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),0),str)
Date_np=convert_date_str_array_to_NP_object(date_str=Date0,fmt="%d/%m/%Y %H:%M")
foo=dt_of_numpy_breakdown(Date_np)
heure=column(foo,3)
day=column(foo,2)
mois=column(foo,1)
annee=column(foo,0)

Total_rain=np.array(column(Personal_file_read_function(path="Input/data_meteo.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),6),float)

ET0=np.array(column(Personal_file_read_function(path="Temp/ReferenceEvapotranspiration.csv",
    nbr_lignes_header=1,nbr_lignes_a_lire=0,
    separator=";"),1),float)
path_to_input=("Input/rfumax.txt")
rfumax=np.loadtxt("Input/rfumax.txt",skiprows=1) 
Kc=np.loadtxt("Input/crop_coef.txt",skiprows=1) # Taking into account the crop coefficient
ET0=ET0*Kc # Taking into account the corp coefficient
nn=1 #legacy parameter


#CALCULATION OF RECHARGE BY THE METHOD FROM DOURADO & NETO
Recharge=np.full((nn,len(Total_rain)),0.0)
for i0 in range(0,nn,1):
    #calcul de la recharge sur matrice par thornwaite et mather
    Total_rain_minus_ruis=Total_rain #Pas de ruissellement
    Pb_minus_ruiss_minus_ETP=Total_rain_minus_ruis-ET0
    RFU=np.array([0.0]*len(Pb_minus_ruiss_minus_ETP))
    APWL=np.array([0.0]*len(Pb_minus_ruiss_minus_ETP))
    ETR=np.array([0.0]*len(Pb_minus_ruiss_minus_ETP))
    RFU[0]=rfumax
    APWL[0]=0.0
  
    for i in range(1,len(Pb_minus_ruiss_minus_ETP),1):
    #APWL
        if (Pb_minus_ruiss_minus_ETP[i]>0):
            if (RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]>rfumax):
                APWL[i]=0.0
            else:
                APWL[i]=-rfumax*np.log((RFU[i-1]+Pb_minus_ruiss_minus_ETP[i])/rfumax)
        else:
            APWL[i]=APWL[i-1]-Pb_minus_ruiss_minus_ETP[i]

    #RFU
        if  (Pb_minus_ruiss_minus_ETP[i]>0):
            if(RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]>rfumax):
                expr1=rfumax
            else:
                expr1=RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]
        else:
            expr1=rfumax*np.exp(-(APWL[i]/rfumax))
            
        if (expr1<0):
                RFU[i]=0.0
        else:
                RFU[i]=expr1

    #RECHARGE
        if(Pb_minus_ruiss_minus_ETP[i]>0):
            ETR[i]=ET0[i]
            if(RFU[i-1]+Pb_minus_ruiss_minus_ETP[i]>rfumax):
                    Recharge[i0,i]=Pb_minus_ruiss_minus_ETP[i]-(RFU[i]-RFU[i-1])
            else:
                Recharge[i0,i]=0.0
        else:
            ETR[i]=Total_rain_minus_ruis[i]-(RFU[i]-RFU[i-1])
            Recharge[i0,i]=0.0
            
    #WRITING OF OUTPUTS
    h=open("Output.csv","w")
    nom=[]
    nom.append("Date")
    nom.append("Total Rain (mm/h)")
    nom.append("Reference ET (mm/h)")
    nom.append("Potential ET (mm/h)")
    nom.append("Actual ET (mm/h)")
    nom.append("Recharge (mm/h)")
    for i in range(0,len(nom),1):
        if (i< len(nom)-1):
            h.write(str(nom[i])+";")
        else:
            h.write(str(nom[i])+"\n")
            
    for i in range(0,len(Date_np),1):
        h.write(str(Date0[i])+";")
        h.write(str(Total_rain[i])+";")
        h.write(str(ET0[i]/Kc)+";")
        h.write(str(ET0[i])+";")
        h.write(str(ETR[i])+";")
        h.write(str(Recharge[i0,i])+"\n")
    h.close()


    #PLOT OF ACTUAL AND POTENTIAL ET
    fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    #fig.suptitle("Modele d'interactions piezomètre/fracture et matrice\n",y=0.98)
    fig.supylabel("Evapotranspiration (mm/h)",x=-0.0,size=14)
    fig.supxlabel('Date',y=-0.13,size=14)
    y1 =ET0
    x1 =Date_np
    ax.plot(x1, y1, label = "Potential",color="black")
    y1 =ETR
    x1 =Date_np
    ax.plot(x1, y1, label = "Actual",color="red")
    ax.legend(loc='lower left',bbox_to_anchor=(0.03, 0.8),ncol=1, prop={'size': 12})

    ax.tick_params(axis='x', which='major', labelsize=12)
    ax.tick_params(axis='y', which='major', labelsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(range(1,13,1))))
    ax.xaxis.set_minor_locator(mdates.MonthLocator([1,4,7,10]))
    for label in ax.get_xticklabels(which='major'):label.set(rotation=90)
    #ax.set_ylim(440,446)
    plt.savefig("ET.png",bbox_inches='tight')
    plt.close()

    #PLOT OF TOTAL RAIN AND ACTUAL RECHARGE
    fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    #fig.suptitle("Modele d'interactions piezomètre/fracture et matrice\n",y=0.98)
    fig.supylabel("Intensity (mm/h)",x=-0.0,size=14)
    fig.supxlabel('Date',y=-0.13,size=14)
    y1 =Total_rain
    x1 =Date_np
    ax.plot(x1, y1, label = "Total rain",color="black")
    y1 =Recharge[i0,:]
    x1 =Date_np
    ax.plot(x1, y1, label = "Actual recharge",color="red")
    ax.legend(loc='lower left',bbox_to_anchor=(0.03, 0.8),ncol=1, prop={'size': 12})

    ax.tick_params(axis='x', which='major', labelsize=12)
    ax.tick_params(axis='y', which='major', labelsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(range(1,13,1))))
    ax.xaxis.set_minor_locator(mdates.MonthLocator([1,4,7,10]))
    for label in ax.get_xticklabels(which='major'):label.set(rotation=90)
    #ax.set_ylim(440,446)
    plt.savefig("Recharge.png",bbox_inches='tight')
    plt.close()


print("**ACTUAL EVAPOTRANSPIRATION AND RECHARGE CALCULATED SUCCESSFULLY**")
time.sleep(1)



