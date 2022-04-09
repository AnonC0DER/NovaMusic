from telebot import types, TeleBot
from config import BOT_TOKEN, BOT_USERNAME, SUDO
from db import Add_new_song, Search_In_All_Songs, Count_songs, Get_music_name
from utils import Get_users_count, Write_userID, is_user, Get_total_users, Get_lyrics


# Set Up
bot = TeleBot(token=BOT_TOKEN)


# Start message
@bot.message_handler(commands=['start'])
def Start_handler(message):
    '''Start message handler'''
    if message.chat.type == 'private':
        # Write user id in txt file if it doesn't exists
        if is_user(message.from_user.id, 'members') == False:
            Write_userID(message.from_user.id, 'members')
        
        else:
            pass
        
        command = message.text.replace('/start ', '')
        if command == '/start' or 'online' in command:
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

        else:
            music_name = Get_music_name(command)
            lyrics = Get_lyrics(music_name[0])
            if lyrics == 'Not Found':
                bot.reply_to(message, 'Sorry I couldnot find lyrics.', 
                reply_markup=types.InlineKeyboardMarkup(
                    [ 
                        [
                            types.InlineKeyboardButton(
                                '🎵 Search again 🎵', switch_inline_query_current_chat='')
                        ]
                    ]
            ))

            else:
                bot.reply_to(message, f'Lyrics found by [NovaMusic](https://t.me/{BOT_USERNAME})\n\n{lyrics}',
                reply_markup=types.InlineKeyboardMarkup(
                    [ 
                        [
                            types.InlineKeyboardButton(
                                '🎵 Search music 🎵', switch_inline_query_current_chat='')
                        ]
                    ]
                ), parse_mode='markdown')

# Ping Pong
@bot.message_handler(commands=['ping', f'ping@{BOT_USERNAME}'])
def PingPong_handler(message):
    '''PingPong handler'''
    
    # Write user id in txt file if it doesn't exists
    if is_user(message.from_user.id, 'members') == False:
            Write_userID(message.from_user.id, 'members')
        
    else:
        pass

    bot.send_message(message.chat.id, 'Pong 🏓', reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton('🎵 Search music 🎵', switch_inline_query_current_chat='')]
    ]), reply_to_message_id=message.message_id)


# Add music
@bot.message_handler(content_types=['audio'])
def Add_Music(message):
    '''Add music to database'''

    if message.chat.type == 'private':
        # Write user id in txt file if it doesn't exists
        if is_user(message.from_user.id, 'members') == False:
            Write_userID(message.from_user.id, 'members')
        
        else:
            pass

        # There is msuic title and music performer
        if message.audio.title and message.audio.performer:
            Add_new_song(message.audio.title.lower(), message.audio.performer.lower(), 
                        message.audio.file_id, message.audio.file_unique_id)

            bot.reply_to(message, '[+] Added to database')

        else:
            bot.reply_to(message, '[❌] Something is wrong with the given audio.')
            

#################################### Inline - Only sudo & admin
# Get statistics
@bot.inline_handler(lambda query: query.query == '!stat')
def Get_stat_inline(chosen_inline_result):
    '''Get robot statistics using inline queries'''

    # Sudo and admins can delete music
    if str(chosen_inline_result.from_user.id) == SUDO:
        count_songs = Count_songs()
        result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent(f'''
📊 Statistics 📊

🎧 All music : {count_songs[0]}
👥 All users : {Get_total_users()}
👥 Users : {Get_users_count('members')}
👥 Inline users : {Get_users_count('inline_members')}
🔆 Admins : {len([SUDO])}

[Github](https://github.com/AnonC0DER/NovaMusic)''', parse_mode='markdown'))

        bot.answer_inline_query(chosen_inline_result.id, [result], cache_time=1)
#################################### Inline - users
# Show robot is Up
@bot.inline_handler(lambda query: len(query.query) == 0 or query.query == None)
def RobotUp_handler(chosen_inline_result):
    '''Show robot is Up'''

    # Write user id in txt file if it doesn't exists
    if is_user(chosen_inline_result.from_user.id, 'inline_members') == False:
        if is_user(chosen_inline_result.from_user.id, 'members') == False:
            Write_userID(chosen_inline_result.from_user.id, 'inline_members')
        
    else:
        pass

    result = None
  
    bot.answer_inline_query(chosen_inline_result.id, results=[result], 
    switch_pm_text="I'm online !", switch_pm_parameter='online')


# Inline music search
@bot.inline_handler(lambda query: query.query)
def Search_music(chosen_inline_result):
    '''Search music and return it for user'''
    
    # Write user id in txt file if it doesn't exists
    if is_user(chosen_inline_result.from_user.id, 'inline_members') == False:
        if is_user(chosen_inline_result.from_user.id, 'members') == False:
            Write_userID(chosen_inline_result.from_user.id, 'inline_members')
        
    else:
        pass

    # Get query
    query = chosen_inline_result.query.lower()

    results = []    
    music_id = 0
    # Get results from database
    results_from_db = Search_In_All_Songs(query)
    
    try:
        for song in results_from_db:
            music_id += 1
            results.append(
                types.InlineQueryResultAudio(str(music_id), song[2], song[0],
                caption=f'[NovaMusic](https://t.me/{BOT_USERNAME})', parse_mode='markdown',
                reply_markup=types.InlineKeyboardMarkup(
                [ 
                    [
                        types.InlineKeyboardButton(
                            '🎸 Lyrics  🎸', url=f'https://t.me/{BOT_USERNAME}?start={song[3]}')
                    ]
                ]
            )))

        if len(results) != 0:
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
    
    except:
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
        
    

# Get Statistics
@bot.message_handler(commands=['stat', f'stat@{BOT_USERNAME}'])
def Stat_handler(message):
    # If user is admin
    if str(message.from_user.id) == SUDO:
        count_songs = Count_songs()

        bot.reply_to(message, f'''
📊 Statistics 📊

🎧 All music : {count_songs[0]}
👥 All users : {Get_total_users()}
👥 Users : {Get_users_count('members')}
👥 Inline users : {Get_users_count('inline_members')}
🔆 Admins : {len([SUDO])}

[Github](https://github.com/AnonC0DER/NovaMusic)''', parse_mode='markdown')


print('[+] Robot started successfully !')
bot.polling(none_stop=True)