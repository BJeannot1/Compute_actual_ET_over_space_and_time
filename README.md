### This repository presents a bot I made that plays the telgram lumberjack game. To the best of my knowledge, this is the best bot on the internet for this game (Average score around 1050).

# **I.	Quick description of the game**

In this game, the user plays as a lumberjack cutting an infinitely tall tree. The goal is to chop the highest possible amount of wood pieces before you run out of time, by choping on either the left or right side of the tree. However, while choping, the lumberjack must also dodge the failing tree branches, by standing on the opposite side of the tree. Touching a branch leads to a game over. An image from the game is shown below.

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
  
