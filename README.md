### This repository presents a python progam I made in order to compute actual evapotranspiration and actual recharge to the groundwater, at a hourly time step.
Calculation of reference and potential evapotranspiration follows the guidelines of 

# **I.	INPUTS**

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


![alt text](https://github.com/BJeannot1/Telegram-lumberjack-game-bot/blob/master/illustration.png?raw=true)

The game can be played [here](https://tbot.xyz/lumber/#eyJ1IjoxMTgyMDUxMTQ2LCJuIjoiQmVuemkgSiIsImciOiJMdW1iZXJKYWNrIiwiY2kiOiIzOTc5NTU4MzQ2NjExMDk2MTc3IiwiaSI6IkJBQUFBQVFBQUFCS3EzUkcySjFGSTBsTEhYYyJ9NmUxMzA4ZjVmYTFjMmVhNWVkYTQ5NzEyNzVjYzJlN2I=&tgShareScoreUrl=tg%3A%2F%2Fshare_game_score%3Fhash%3D-D4pwwx_VnDH33gGq6bKWSjcRfgcUMFpmN4_ih_oUfc).

# **II.	Bot playing the game**
  ## 1. Principle
The bot screens the color of specific pixels on each side of the tree, and uses these information in order to determine on what side of the tree to chop.
 ## 2.Required librairies

The bot uses the following python libraries :
- selenium, win32api and win32 con, for automation purposes
- numpy, for reading the file of parameters
- pyautoguy, for saving images of the screen and analyzing pixels color
- shutil, for deleting the folder that stores all the temporary images created when running the code

## 3. Limitations
  
- This is a bot working on Windows only
- You need Firefox installed
- The default parameters are adapted only for a resolution of 1920*1080. You can change the values in the file parameters.txt to adapt the bot to other screen resolutions

## 4. Performance
Here is a video showing off the performance of the code :



https://user-images.githubusercontent.com/67539849/182007653-762bd172-7fd7-4c6b-a4e7-acadfeda02ca.mov


The bot's performance compared to others on the internet comes from the fact it uses a single image to decide about the next 5 to 6 moves, by screening different pixels at the same time, while other codes usually use a given image to decide only about the next move.

  ## 5. Using the bot
  Download the repository and run Main.py. That is it !
  
