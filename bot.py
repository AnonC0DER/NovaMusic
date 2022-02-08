from telebot import types, TeleBot
from redis import Redis 
from config import BOT_TOKEN, BOT_USERNAME, REDIES_PASSWORD, REDIES_PORT, REDIES_SERVER, SUDO, GENIUS_TOKEN
from utils import Get_users_count, Write_userID, is_user, Get_total_users, Get_lyrics


# Set Up
bot = TeleBot(token=BOT_TOKEN)
Rr = Redis(host=REDIES_SERVER, port=REDIES_PORT, password=REDIES_PASSWORD, decode_responses=True)


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
        if command == '/start':
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
            command = command.replace('_', ' ')
            lyrics = Get_lyrics(command)
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
        


#################################### Inline - Only sudo & admin
# Add a new admin using inline queries, Only sudo
@bot.inline_handler(lambda query: '!add ' in query.query)
def Add_admin(chosen_inline_result): 
    '''Add a new admin - type @BOT_USERNAME !add USERID'''
    
    # Only sudo can use this
    if str(chosen_inline_result.from_user.id) == SUDO:
        admin_userid = chosen_inline_result.query.replace('!add ', '')
        if str(admin_userid) not in Rr.lrange('Admin', 0, -1):
            Rr.lpush('Admin', admin_userid)
            result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent(f'[+] {admin_userid} was added to admin list successfully.'))

        else:
            result = types.InlineQueryResultArticle('1', 'Already in database !', types.InputTextMessageContent('This user is already admin !'))

        bot.answer_inline_query(chosen_inline_result.id, [result], cache_time=1)
    
    else:
        pass


# Return admin user IDs
@bot.inline_handler(lambda query: query.query == '!alist')
def Admin_list(chosen_inline_result):
    '''Return a list of admin user IDs'''
    
    # Only sudo can use this
    if str(chosen_inline_result.from_user.id) == SUDO:
        query = Rr.lrange('Admin', 0, -1)
        Admins = []

        for admin in query:
            Admins.append(f'tg://openmessage?user_id={admin}')

        result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent(f'Admin List :\n\n{Admins}'))

        bot.answer_inline_query(chosen_inline_result.id, [result], cache_time=1)


# Delete a admin
@bot.inline_handler(lambda query: '!del ' in query.query)
def Delete_Admin(chosen_inline_result):
    '''Delete a admin - type @BOT_USERNAME !del USERID'''

    # Only sudo can use this
    if str(chosen_inline_result.from_user.id) == SUDO:
        admin_userid = chosen_inline_result.query.replace('!del ', '')
        try:
            Rr.lrem('Admin', 0, admin_userid)
            result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent(f'[+] {admin_userid} was successfully deleted.'))
        
        except Exception as e:
            result = types.InlineQueryResultArticle('1', 'Something went wrong !', types.InputTextMessageContent(f'Error :\n\n{e}'))

        bot.answer_inline_query(chosen_inline_result.id, [result])


# Delete all admins
@bot.inline_handler(lambda query: query.query == '!delall')
def Delete_all_admins(chosen_inline_result):
    '''Delete all admins'''

    # Only sudo can use this
    if str(chosen_inline_result.from_user.id) == SUDO:
        Rr.delete('Admin')
        result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent('Admin list was cleared !'))

        bot.answer_inline_query(chosen_inline_result.id, [result], cache_time=1)


# Delete music
@bot.inline_handler(lambda query: '!dm ' in query.query)
def Delete_music(chosen_inline_result):
    '''Delete music'''
    
    # Sudo and admins can delete music
    if str(chosen_inline_result.from_user.id) == SUDO or str(chosen_inline_result.from_user.id) in Rr.lrange('Admin', 0, -1):
        music_name = chosen_inline_result.query.replace('!dm ', '').lower()
        delete_music = Rr.hdel('Music', music_name)
        if delete_music == 1:
            result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent(f'[+] {music_name} was successfully deleted.'))
        
        else:
            result = types.InlineQueryResultArticle('1', 'Something went wrong !', types.InputTextMessageContent(f'I couldnot delete {music_name}.\nCheck the name, make sure you type it correctly.'))

        bot.answer_inline_query(chosen_inline_result.id, [result])


# Get statistics
@bot.inline_handler(lambda query: query.query == '!stat')
def Get_stat_inline(chosen_inline_result):
    '''Get robot statistics using inline queries'''

    # Sudo and admins can delete music
    if str(chosen_inline_result.from_user.id) == SUDO or str(chosen_inline_result.from_user.id) in Rr.lrange('Admin', 0, -1):
        result = types.InlineQueryResultArticle('1', 'Done', types.InputTextMessageContent(f'''
📊 Statistics 📊

🎧 All music : {len(Rr.hgetall('Music'))}
👥 All users : {Get_total_users()}
👥 Users : {Get_users_count('members')}
👥 Inline users : {Get_users_count('inline_members')}
👤 Admins : {Rr.llen('Admin')}
🔆 Sudo : {len([SUDO])}

[Github](https://github.com/AnonC0DER/NovaMusic)''', parse_mode='markdown'))

        bot.answer_inline_query(chosen_inline_result.id, [result], cache_time=1)
#################################### Inline - users
# Return music when user is not searching
@bot.inline_handler(lambda query: len(query.query) == 0 or query.query == None)
def RetrunMusic_handler(chosen_inline_result):
    '''Return 16 results from music database'''

    # Write user id in txt file if it doesn't exists
    if is_user(chosen_inline_result.from_user.id, 'inline_members') == False:
        if is_user(chosen_inline_result.from_user.id, 'members') == False:
            Write_userID(chosen_inline_result.from_user.id, 'inline_members')
        
    else:
        pass

    music_id = 0
    results = []
    for music in Rr.hgetall('Music'):
        # Return 16 results each time
        if len(results) <= 15:
            music_id += 1
            # Replace all spaces with _ and remove all ()
            lyrics = music.replace('(', '')
            lyrics = music.replace(')', '')
            lyrics = music.replace(' ', '_')
            # Append music to results list
            results.append(types.InlineQueryResultAudio(str(music_id), Rr.hgetall('Music').get(music), music, 
            caption=f'[NovaMusic](https://t.me/{BOT_USERNAME})', parse_mode='markdown',
            reply_markup=types.InlineKeyboardMarkup(
                [ 
                    [
                        types.InlineKeyboardButton(
                            '🎸 Lyrics  🎸', url=f'https://t.me/{BOT_USERNAME}?start={lyrics}')
                    ]
                ]
                ))) 

    bot.answer_inline_query(chosen_inline_result.id, results)


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


    # Search in database
    for music in Rr.hgetall('Music'):
        # 50 inline results are acceptable each time
        if len(results) <= 49:
            # If query in music title
            if query in music:
                # Replace all spaces with _ and remove all ()
                lyrics = music.replace('(', '')
                lyrics = music.replace(')', '')
                lyrics = music.replace(' ', '_')
                music_id += 1
                # Append it to results list
                results.append(
                    types.InlineQueryResultAudio(str(music_id), Rr.hgetall('Music').get(music), music,
                    caption=f'[NovaMusic](https://t.me/{BOT_USERNAME})', parse_mode='markdown',
                    reply_markup=types.InlineKeyboardMarkup(
                [ 
                    [
                        types.InlineKeyboardButton(
                            '🎸 Lyrics  🎸', url=f'https://t.me/{BOT_USERNAME}?start={lyrics}')
                    ]
                ]
                )))
                    
        else:
            break
        
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
    
    

# Get Statistics
@bot.message_handler(commands=['stat', f'stat@{BOT_USERNAME}'])
def Stat_handler(message):
    # If user is admin
    if str(message.from_user.id) in Rr.lrange('Admin', 0, -1) or str(message.from_user.id) == SUDO:
        bot.reply_to(message, f'''
📊 Statistics 📊

🎧 All music : {len(Rr.hgetall('Music'))}
👥 All users : {Get_total_users()}
👥 Users : {Get_users_count('members')}
👥 Inline users : {Get_users_count('inline_members')}
👤 Admins : {Rr.llen('Admin')}
🔆 Sudo : {len([SUDO])}

[Github](https://github.com/AnonC0DER/NovaMusic)''', parse_mode='markdown')







print('[+] Robot started successfully !')
bot.polling(none_stop=True)