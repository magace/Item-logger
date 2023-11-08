# Item logger
 Sends specific loot from Kolbot to discord

Basically we are going to make kolbot save images of everything it loots.
Next the python script will parse the folder(s) images and check if the name matches one of the lines in match.txt.
If it does it will send the image to the discord hook specified in the config.

How to setup:
Install Python and pip install required libs.
Edit config.js, you will need to enter your discord webhook here, as well as set the path to kolbots images folder. 
Make sure to use double back slashes.
Edit match.txt here you will enter any item names you actually want to send to discord.  I personally didn't want every single item it finds sending.


Kolbot:  Locate and open Item.js (d2bs/kolbot/libs/core/item.js)
Search for "D2Bot.printToItemLog(itemObj);"
Directly above that add this line: "D2Bot.saveItem(itemObj);"
Another thing you can do is add me.profile to keptline to see what profile found what like so: 
"keptLine && (desc += ("\n\\xffc0Line: " + keptLine + " " + me.profile));"

Run the python script and wait for images to appear.
