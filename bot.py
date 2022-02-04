from telebot import telebot, types
from redis import Redis 
from config import BOT_TOKEN, BOT_USERNAME, REDIES_PASSWORD, REDIES_PORT, REDIES_SERVER


# Set Up
bot = telebot.TeleBot(token=BOT_TOKEN)
Rr = Redis(host=REDIES_SERVER, port=REDIES_PORT, password=REDIES_PASSWORD, decode_responses=True)


# Start message
@bot.message_handler(commands=['start', f'start@{BOT_USERNAME}'])
def Start_handler(message):
    '''Start message handler'''

    bot.reply_to(message, f'''
Hello, I'm Nova.
You can search and get your favorite music using me.
Use this buttons (b) or type "@{BOT_USERNAME} music" and enter your music name to get it.''', 
    reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton('Search', switch_inline_query_current_chat='music')]
    ]))



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

    # Return music 
    bot.answer_inline_query(chosen_inline_result.id, results)



bot.polling(none_stop=True)