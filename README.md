### This repository presents a python progam I made in order to compute actual evapotranspiration and actual recharge to the groundwater, at a hourly time step and in a spatially distributed way.

# **I.	Introduction**

Calculation of reference and potential evapotranspiration follows the guidelines of FAO Irrigation and Drainage Paper No. 56, whose title is "Crop
Evapotranspiration (guidelines for computing crop water requirements)". Calculation of actual evapotranspiration from potential evapotranspiration and recharge follows the method used by Dourado-Neto et al.(2010).

**Sample outputs from the code, using the example input file :**

- Computed actual evapotranspiration at a given date over an area covering parts of France, Germany, Italy, and Switzeland, based on a synthetic dataset :

![map_3500](https://user-images.githubusercontent.com/67539849/184679707-7fa19ae4-24de-42d8-a297-5ed89b4b0669.png)
- Comparison of potential and actual evapotranspiration at given coordinates for year 2016, based on a synthetic dataset :

![Output_Potential ET_Actual ET](https://user-images.githubusercontent.com/67539849/184679733-72a50352-8cb0-4bbb-831a-2d7732066ad6.png)
- Comparison of total rain and actual gorundwater recharge at given coordinates for year 2016, based on a synthetic dataset :

![Output_Total rain_Recharge](https://user-images.githubusercontent.com/67539849/184679737-ac805174-6f44-4388-b0a8-2af7a938247e.png)

# **II.	Inputs**

All the inputs are to be found in a single netCDF file, named "Inputs.nc". These inputs are the following :
- Latitudes (in °N) and longitudes (in °W);
- Longitude of the centre of the time zone  in °W);
- Time, expressed in the following way : "%d/%m/%Y %H:%M";
- Distributed hourly average temperature (°C);
- Distributed hourly Wind speed at 10 m (m/s);
- Distirbuted hourly Atmospheric pressure (hPa);
- Distributed hourly relative humidity (%);
- Distirbuted hourly total rain (mm/h);
- Distributed hourly global radiation (also called solar radiation) in joules/cm²;
- Distributed hourly total available water in the root zone in conditions of full saturation (mm);
- Distirbuted crop coefficient, defining the ratio between reference and potential evapotranspiration. The reference evapotranspiration corresponds to the potential evapotranspiration of a reference crop of height 12cm, albedo 0.23 and surface resistance of 70 s m-1.

An example dataset is provided in this repository. Refer to this file for more details about input formatting.

# **III.	Running the code**
  ## 1. Requirements
The most updated versions of the following libraries must be installed to run the code successfully :
- netCDF4
- numpy
- datetime
- re
- matplotlib

 ## 2. Steps
- Download the repository;
- Replace the example input file by a netCDF file describing the settings of your test case;
- Run "Main.py".

 ## 3. Outputs
Running the code generates several outputs :
- An Output.nc netcdf file, containing distributed hourly time series of potential and actual ET, of total precipitation and actual recharge to the groundwater;
- A map displaying the spatial repartition of actual evapotranspiration (cf. introduction);
- 2 plots showing time series respectively of potential VS actual evapotranspiration and total rain VS actual recharge (cf. introduction).
  
# **IV.	Cited bibliography**
  
Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements. FAO Irrigation and Drainage Paper. Food and Agriculture Organization (FAO), Rome, Italy, 300 pp.

Dourado-Neto, D., Van Lier, QdJ., Metselaar, K., Reichardt, K., Nielsen, D.R., 2010. General procedure to initialize the cyclic soil water balance by the Thronthwaite and Mather method. Scientia Agricola 67, 87-95.
  
