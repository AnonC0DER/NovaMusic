# NovaMusic

## Summary
NovaMusic is a music sharing robot. Users can get music and music lyrics using inline queries. <br>
Users can send music to robot and robot saves the music in the database. <br>
This is how music database grows up. <br>
I used Redis nosql database for this project. <br>
You can create a free Redis online database, use this [link](https://app.redislabs.com/).


## Plans
- [ ] Create lyricsfreak.com API


# Setting up things

## Environment
Create a file named `.env` in the directory and add all the variables there. An example of `.env` file:
```
API_ID = Your API ID
API_HASH = Your API hash
BOT_TOKEN = Robot token
SUDO = Put sudo user chat id here
BOT_USERNAME = Put robot username
REDIES_SERVER = Redis server
REDIES_PASSWORD = xxxxxxxx
REDIES_PORT = Put your port
```


## Commands
1. `pip install -r requirements.txt`
2. `python bot.py`
