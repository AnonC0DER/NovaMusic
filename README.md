# [NovaMusic](https://t.me/NovaMusicRobot)

## Summary
NovaMusic is a music sharing robot. Users can get music and music lyrics using inline queries. <br>
Users can send music to robot and robot saves the music in the database. <br>
This is how music database grows up. <br>
I used Redis nosql database (postgresql in new version) in this project. <br>
You can create a free Redis online database, use this [link](https://app.redislabs.com/).


## Plans
- [x] Create lyricsfreak.com API Done -> [LyricsFk](https://github.com/AnonC0DER/lyricsfreak-api)


# Setting up things

## Environment
Create a file named `.env` in the directory and add all the variables there. An example of `.env` file:
```
BOT_TOKEN = bot token
SUDO = sudo chat id
BOT_USERNAME = robot username
DB_HOST = db host
DB_DATABASE = db name
DB_USER = db user
DB_PASSWORD = db pass
```


## Commands
1. `pip install -r requirements.txt`
2. `python bot.py`
