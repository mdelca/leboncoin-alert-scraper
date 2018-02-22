# Leboncoin.fr alert scraper

Because [leboncoin](leboncoin.fr) doesn't provide a real time alert system, the goal of this project is to create your own, to be notified when a new ad is available.

### Requirements
* This project depends on Python3.4 and newer, be careful of which version of python you are using
* Then install the requirements with this command : ```pip install -r requirements.txt```

### Instructions
Go check the file [settings.py](https://github.com/UzfulLab/leboncoin-alert-scraper/blob/master/settings.py) and add your own settings :
* To find the url of your need, just go on [leboncoin](leboncoin.fr) website, make a search of whatever you want, and copy and paste the url in the corresponding setting parameter. You can add has many urls as you want.
* Then, fill the informations about the email details, receiver, sender, etc.

Once requirements satisfied, the idea is to run the script on a server, using a cron job.

To do so :
 * ```ssh``` to your server
 * ```git clone``` this project
 * install the requirements ```pip3 install -r requirements.txt``` (you might need ```sudo```)
 * add your settings
 * create a new cronjob ```crontab -e```
 * add a line like ```* * * * * /path/to/your/python/executable /home/user/path/to/the/script/main.py```
 Like this the script will be executed every minute
 * exit the crontab with ```ctrl + x``` if you use nano editor, and you're good to go !


### Troubleshooting with Gmail
To enable Gmail to send you email throught this app, you'll have to active the ```Less secure app``` option in your Google account has described in this [stackoverflow thread](http://stackoverflow.com/a/27515833).
