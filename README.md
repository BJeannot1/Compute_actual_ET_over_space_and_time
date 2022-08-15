### This repository presents a python progam I made in order to compute actual evapotranspiration and actual recharge to the groundwater, at a hourly time step and in a spatially distributed way.
Calculation of reference and potential evapotranspiration follows the guidelines of FAO Irrigation and Drainage Paper No. 56, whose title is "Crop
Evapotranspiration (guidelines for computing crop water requirements)". Calculation of actual evapotranspiration from potential evapotranspiration and recharge follows the method used by Dourado-Neto et al.(2010)

**Sample outputs from the code :**

- Computed actual evapotranspiration at a given date over an area covering parts of France, Germany, Italy, and Switzeland, based on a synthetic dataset :
![map_3500](https://user-images.githubusercontent.com/67539849/184679707-7fa19ae4-24de-42d8-a297-5ed89b4b0669.png)
- Comparaison of potential and actual evapotranspiration at given coordinates for year 2016, based on a synthetic dataset :
![Output_Potential ET_Actual ET](https://user-images.githubusercontent.com/67539849/184679733-72a50352-8cb0-4bbb-831a-2d7732066ad6.png)
- Comparaison of total rain and actual gorundwater recharge given coordinates for year 2016, based on a synthetic dataset :
![Output_Total rain_Recharge](https://user-images.githubusercontent.com/67539849/184679737-ac805174-6f44-4388-b0a8-2af7a938247e.png)

# **I.	Inputs**

The input files and their expected content are :
## 1. Input file data_meteo.csv
- Hourly average temperature (°C)
- Hourly Wind speed at 10 m (m/s)
- Hourly Atmospheric pressure (hPa)
- Hourly relative humidity (%)
- Hourly total rain (mm/h)
- Hourly global radiation (also called solar radiation) in joules/cm²
## 2. Input file localisation_site.csv
- latitude and longitude of studied site (°N and °O)
- longitude of centre of the time zone of the studied site (°O)
## 3. Input file RFUMAX.txt
- Total available water in the root zone when it is fully saturated (mm)
## 4. Input file crop_coef.txt
- Crop coefficient, defining the ratio between reference and potential evapotranspiration. The reference evapotranspiration corresponds to the potential evapotranspiration of a reference crop of height 12cm, albedo 0.23 and surface resistance of 70 s m-1

An example dataset is provided in the "Inputs" folder of this repository.

# **II.	Running the code**
  ## 1. Requirements
The most updated versions of thefollowing libraries must be installed to run the code successfully :
- numpy
- datetime
- re
- matplotlib

 ## 2. Steps
- Download the repository
- Replace the example files in the "Inputs" folder by inputs files corresponding to your study site
- Run "Main.py"
- This generates two image outputs (ET.png and Recharge.png) and also a file Outputs.csv, displaying the computed hourly time series of actual evapotranspiration and recharge
  
 ## 3. Cited bibliography
  
Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements. FAO Irrigation and Drainage Paper. Food and Agriculture Organization (FAO), Rome, Italy, 300 pp.

Dourado-Neto, D., Van Lier, QdJ., Metselaar, K., Reichardt, K., Nielsen, D.R., 2010. General procedure to initialize the cyclic soil water balance by the Thronthwaite and Mather method. Scientia Agricola 67, 87-95.
  
