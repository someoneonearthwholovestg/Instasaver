#!/bin/bash
# returns count of files in dir
#ls -1 | wc -l

# screen proccesses are here
#/var/run/screen/S-root

# if count of screen proccesses is 0, then run bot
if [ $(ls -1 /var/run/screen/S-root | wc -l) -eq 0 ]
then
    source /home/instasaver/venv/bin/activate && screen -d -m python3 /home/instasaver/instasaver/instaBot.py
fi

# chmod +x checkBot.sh
# -**- in crontab write the following: -**-
#  * * * * * /home/instasaver/checkBot.sh
