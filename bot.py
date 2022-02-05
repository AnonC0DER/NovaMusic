from telebot import types, TeleBot
from redis import Redis 
from config import BOT_TOKEN, BOT_USERNAME, REDIES_PASSWORD, REDIES_PORT, REDIES_SERVER


# Set Up
# bot = telebot.TeleBot(token=BOT_TOKEN)
bot = TeleBot(token=BOT_TOKEN)
Rr = Redis(host=REDIES_SERVER, port=REDIES_PORT, password=REDIES_PASSWORD, decode_responses=True)


# Start message
@bot.message_handler(commands=['start', f'start@{BOT_USERNAME}'])
def Start_handler(message):
    '''Start message handler'''

    bot.reply_to(message, f'''
Hello, I'm Nova.
You can search and get your favorite music using me.
Send your music for me, then you can search it everywhere in your chats and get it :).
Use this buttons ⬇️ or type "@{BOT_USERNAME} music" and enter your music name to get it.''', 
    reply_markup=types.InlineKeyboardMarkup(
            [ 
                [
                    types.InlineKeyboardButton(
                        '🎵 Search music 🎵', switch_inline_query_current_chat='')
                ],[
                    types.InlineKeyboardButton(
                        'Github', url='https://github.com/AnonC0DER/NovaMusic')
                ]
            ]
    ))


# Ping Pong
@bot.message_handler(commands=['ping', f'ping@{BOT_USERNAME}'])
def PingPong_handler(message):
    '''PingPong handler'''
    
    bot.reply_to(message, 'Pong 🏓', reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton('🎵 Search music 🎵', switch_inline_query_current_chat='')]
    ]))


# Add music
@bot.message_handler(content_types=['audio'])
def Add_Music(message):
    '''Add music to database'''

    # There is msuic title and music performer
    if message.audio.title and message.audio.performer:
        if f'{message.audio.title.lower()} {message.audio.performer.lower()}' not in Rr.hgetall('Music'):
            Rr.hset('Music', f'{message.audio.title.lower()} {message.audio.performer.lower()}', message.audio.file_id)

            bot.reply_to(message, '[+] Added to database')
        
        else:
            bot.reply_to(message, '[-] Already in database')

    # There is only msuic title
    elif message.audio.title:
        if f'{message.audio.title.lower()} unknown' not in Rr.hgetall('Music'):
            Rr.hset('Music', f'{message.audio.title.lower()} unknown', message.audio.file_id)

            bot.reply_to(message, '[+] Added to database')
        
        else:
            bot.reply_to(message, '[-] Already in database')

    # There is no msuic title and music performer, so add music file name to database
    else:
        if f'{message.audio.file_name.lower()} unknown' not in Rr.hgetall('Music'):
            Rr.hset('Music', f'{message.audio.file_name.lower()} unknown', message.audio.file_id)

            bot.reply_to(message, '[+] Added to database')
        
        else:
            bot.reply_to(message, '[-] Already in database')
        


#################################### Inline
# Inline music search
@bot.inline_handler(lambda query: query.query)
def Search_music(chosen_inline_result):
    '''Search music and return it for user'''
    
    # Get query
    query = chosen_inline_result.query.lower()
    
    results = []
    music_id = 0


    # Search in database
    for music in Rr.hgetall('Music'):
        # If query in music title
        if query in music:
            music_id += 1
            # Append it to results list
            results.append(
                types.InlineQueryResultAudio(str(music_id), Rr.hgetall('Music').get(music), music,
                reply_markup=types.InlineKeyboardMarkup(
            [ 
                [
                    types.InlineKeyboardButton(
                        '🎸 More Music  🎸', url=f'https://t.me/{BOT_USERNAME}')
                ],[
                    types.InlineKeyboardButton(
                        '↪️ Share this music ↩️', switch_inline_query=query)
                ]
            ]
        ))) 

    if len(results) != 0:
        # Return music 
        bot.answer_inline_query(chosen_inline_result.id, results)

    else:
        not_found = types.InlineQueryResultArticle(
        id='1', 
        title='Not Found !',
        input_message_content=types.InputTextMessageContent('I couldnot find this music in my database.\nIf you find it, send it for me then I add it to my database.\nHelp me improve my databse, thanks.'),
        description='Sorry, this music is not in my database.', 
        thumb_url='http://ideyab.site/wp-content/uploads/2020/06/error-404.png',
        reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton('🎵 Search music 🎵', switch_inline_query_current_chat='')]
        ]))

        bot.answer_inline_query(chosen_inline_result.id, [not_found])
    
    

print('[+] Robot started successfully !')
bot.polling(none_stop=True)