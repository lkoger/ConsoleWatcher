# Overview
This script currently only checks Target's site for availability of the Series S, Series X, and a standard gray Nintendo Switch. It does not automatically purchase any of them, but instead notifies you via Discord that they are available. In order for this to work, you'll need a discord server.

## Config Instructions
`discord_webhook` needs to be put in the config file. Otherwise the script just won't work. At the time of writing, instructions for creating a webhook could be found at https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks.

`repeat_delay_minutes` is the amount of time, in minutes, that you want to wait after checking all listed urls before checking their availability again. Default time is 15 minutes. 

`availability_recheck_delay_minutes` is the amount of time, in minutes, that you want to wait before rechecking a url that's already been checked and determined to be available. This is to cut down on spamming your discord channel. Default time is 5 hours (300 minutes).

## Issues
* The script is not robust, and sometimes it'll be run and never correctly identify when a console is available. Restarting it almost always resolves this. And when it starts properly, it seems to be very dependable. I provide no guarantees it'll be sufficient for you.

## Plannned Features
* Support for checking more retail stores than Target. 
* Support for checking PS5 availability.
* Support user-provided urls in the config.json (can be changed in run.py).
* Support checking availability of generic items, instead of just consoles.