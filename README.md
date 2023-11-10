# Item logger
 Sends loot from Kolbot to discord

Basically we are going to make kolbot save images of everything it loots.
Next the python script will parse the folder(s) images and check if the name matches one of the lines in match.txt.
If it does it will send the image to the discord hook specified in the config.

**How to setup:**
Install Python use pip to install required libs.

**Edit config.js**
Enter your Discord hook inside webhook_url

Set your path to kolbot images folder

Set useMatchFile to true or false.  This will display all items you find if set to false.  If set to true it will only show files in match.txt

Set clearD2BotErrors to true or false.  This will pusk "OK" when d2bot popps up the "an error has occured" message when set to true

<hr>

Kolbot Setup:

Locate and open Item.js (d2bs/kolbot/libs/core/item.js)

Search for ```D2Bot.printToItemLog(itemObj);```

Directly above that add this line: ```D2Bot.saveItem(itemObj);```

Another thing you can do is add me.profile to keptline to see what profile found what like so: 

"keptLine && (desc += ("\n\\xffc0Line: " + keptLine + " " + me.profile));"

Run the python script and wait for images to appear.

Images:
![image](https://github.com/magace/Item-logger/assets/7795098/0131c964-e102-4072-b5b8-c0923aaef0a8)
![image](https://github.com/magace/Item-logger/assets/7795098/7769976e-78ad-4774-8b0d-c849603c7942)
