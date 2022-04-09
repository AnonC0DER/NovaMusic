import psycopg2 as pgs
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
######################################### DATABASE 

# Connect to database and create the table

# You may need to use CREATE DATABASE dbname; before you create connection
## Get values from .env file
conn = pgs.connect(
    host=DB_HOST,
    database=DB_DATABASE,
    user=DB_USER,
    password=DB_PASSWORD,
)

# create gigadb and its columns if they don't exists
create_table = '''
    CREATE TABLE IF NOT EXISTS novamusic_bot (
        title varchar(250) NOT NULL,
        performer varchar(250) NOT NULL,
        file_id text UNIQUE NOT NULL,
        file_unique_id text UNIQUE NOT NULL
    );
'''

cur = conn.cursor()
cur.execute(create_table)
conn.commit()
cur.close()


######################################### Functions
def Add_new_song(title, performer, file_id, file_unique_id):
    '''Add songs to database'''
    # Insert values into novamusic_bot table
    insert_into_table = f'''
    INSERT INTO novamusic_bot (title, performer, file_id, file_unique_id)
    VALUES ('{title.replace("'", "''")}', '{performer.replace("'", "''")}', '{file_id}', '{file_unique_id}')
    ON CONFLICT (file_unique_id) DO NOTHING;
    '''

    try:
        cur = conn.cursor()
        cur.execute(insert_into_table, ('novamusic_bot',))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)


def Search_In_All_Songs(q):
    '''Search in all songs'''
    query = f'''SELECT * FROM novamusic_bot WHERE title LIKE '%{q.replace("'", "''")}%' OR performer LIKE '%{q.replace("'", "''")}%' LIMIT 50;'''
    
    try:
        cur = conn.cursor()
        cur.execute(query)
        Get_results = cur.fetchall()
        cur.close()
        return Get_results
    except Exception as e:
        print(e)
    

def Count_songs():
    '''Count songs'''
    query = '''SELECT count(*) AS songs_count FROM novamusic_bot;'''
    
    cur = conn.cursor()
    cur.execute(query)
    Get_result = cur.fetchone()
    cur.close()
   
    return Get_result


def Get_music_name(file_unique_id):
    '''Get music name using file_unique_id'''
    query = f'''SELECT title FROM novamusic_bot WHERE file_unique_id='{file_unique_id}';'''

    cur = conn.cursor()
    cur.execute(query)
    Get_result = cur.fetchone()
    cur.close()
   
    return Get_result