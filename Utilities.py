import datetime as dt
from datetime import datetime
import numpy as np
import re

def Personal_file_read_function(path,nbr_lignes_a_lire=0,nbr_lignes_header=0,separator=r'[\s]+',replace_this=[''],replace_by=['']):  # lit en champ de potentiel en tous points. Hypothèse = noeuds renseignés de 1 à n
    obs_file = open(path, "r")  # ouvrir 
    obs_strings = obs_file.readlines()  # lire 
    obs_file.close()  # fermer 
    if (nbr_lignes_a_lire==0):
        nbr_lignes_a_lire=len(obs_strings)-nbr_lignes_header
    numero_ligne_a_lire = nbr_lignes_header  # initialisation du numéro de ligne à lire (1 en-dessous du numéro réel à lire en premier)
    champ = [''] * (nbr_lignes_a_lire)  # initialisation du vecteur
    index=-1
    for i in range(nbr_lignes_header,nbr_lignes_header+nbr_lignes_a_lire):
        index=index+1
        ligne = (obs_strings[i])
        champ[index] = (re.split(separator,ligne))
        for ir in range (0, len(replace_this),1):
            if (replace_this[ir]!=''):
                for i in range(0,len( champ[index]),1):
                    champ[index][i]=champ[index][i].replace(replace_this[ir],replace_by[ir])            
    return (np.array(champ,dtype=object))


def column(matrix, i):
    return [row[i] for row in matrix]
    
      
def convert_date_str_array_to_NP_object(date_str,fmt="%d/%m/%Y %H:%M"):
    nbr_dates=len(date_str)
    date=['']*nbr_dates
    date_str_usa=['']*nbr_dates
    for i in range(nbr_dates):
        date[i]=datetime.strptime(date_str[i],fmt)
        date_str_usa[i]= date[i].strftime("%Y-%m-%d %H:%M")
    date_np = np.array(date_str_usa, dtype='datetime64')
    return(date_np)


def dt_of_numpy_breakdown(dt):
    """
    Convert array of datetime64 to a calendar array of year, month, day, hour,
    minute, seconds, microsecond with these quantites indexed on the last axis.

    Parameters
    ----------
    dt : datetime64 array (...)
        numpy.ndarray of datetimes of arbitrary shape

    Returns
    -------
    cal : uint32 array (..., 7)
        calendar array with last axis representing year, month, day, hour,
        minute, second, microsecond
    """

    # allocate output 
    out = np.empty(dt.shape + (7,), dtype="u4")
    # decompose calendar floors
    Y, M, D, h, m, s = [dt.astype(f"M8[{x}]") for x in "YMDhms"]
    out[..., 0] = Y + 1970 # Gregorian Year
    out[..., 1] = (M - Y) + 1 # month
    out[..., 2] = (D - M) + 1 # dat
    out[..., 3] = (dt - D).astype("m8[h]") # hour
    out[..., 4] = (dt - h).astype("m8[m]") # minute
    out[..., 5] = (dt - m).astype("m8[s]") # second
    out[..., 6] = (dt - s).astype("m8[us]") # microsecond
    return out
