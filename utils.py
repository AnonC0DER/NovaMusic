from urllib.parse import urlencode, urlunparse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import random


# Get Random useragent
def RandomUSERagent():
    
	fp = open('user_agents.txt', 'r')
	Content = fp.read()
	CoList = Content.split('\n')

	USER_AGENTS_LIST = []
	for i in CoList:
		try:
			USER_AGENTS_LIST.append(i)
		except:
			pass

	return random.choice(USER_AGENTS_LIST)


def Get_users_count(txt):
    '''Get users count'''

    if txt == 'members':
        # Open file
        file = open('Members.txt', 'r')
    
    elif txt == 'inline_members':
        # Open file
        file = open('Inline_Members.txt', 'r')
    
    # Read file
    data = file.read()
    # Split each line
    users = data.split('\n')
    Counter = 0

    # Count users
    for user in users:
        if user:
            Counter += 1
        
    return Counter


def Get_total_users():
    '''Get all users count'''
    Users = Get_users_count('members')
    Inline_users = Get_users_count('inline_members')

    total = Users + Inline_users

    return total



def Write_userID(userid, txt):
    '''Write user ID to txt file'''
    
    if txt == 'members':
        file = open('Members.txt', 'a')
        file.write(str(userid) + '\n')
        file.close()

    elif txt == 'inline_members':
        file = open('Inline_Members.txt', 'a')
        file.write(str(userid) + '\n')
        file.close()
        

def is_user(userid, txt):
    '''If userid isn't in txt file return Flase else True'''
    
    if txt == 'members':
        file = open('Members.txt')
        checker = file.read()
        file.close()

        if str(userid) in checker:
            return True
        
        else:
            return False
        
    elif txt == 'inline_members':
        file = open('Inline_Members.txt')
        checker = file.read()
        file.close()

        if str(userid) in checker:
            return True
        
        else:
            return False


def Get_lyrics(query):
    '''Get lyrics using lyrics freak'''

    lyricsFreak = 'https://www.lyricsfreak.com'
    # Prepare url
    url = urlunparse(('https', 'www.lyricsfreak.com', '/search.php', '', urlencode({'q': query}), ''))
    custom_user_agent = RandomUSERagent()
    # make request
    req = Request(url, headers={'User-Agent': custom_user_agent})
    page = urlopen(req)
    # Read html page
    soup = BeautifulSoup(page.read(), 'lxml')

    # Find links
    links = soup.findAll('a', {'class' : 'song'})
    # Find artists
    artists = soup.findAll('div', {'class' : 'lf-list__cell lf-list__title--secondary'})

    MusicLinks = []
    artistsStr = []

    for music in links:
        MusicLinks.append(music['href'])

    for artist in artists:
        artistsStr.append(artist.text.replace('·     ', ''))
	
    
    try:
        # Prpare url
        WebUrls = [lyricsFreak + MusicLinks[0]]
    
    except:
        pass
    
    # Get new user agent
    custom_user_agent = RandomUSERagent()
    LyricsText = []

    try:
        for url in WebUrls:
            # make request
            req = Request(url, headers={'User-Agent': custom_user_agent})
            page = urlopen(req)
            soup = BeautifulSoup(page.read(), 'lxml')
            lyrictxt = soup.findAll('div', {'class' : 'lyrictxt js-lyrics js-share-text-content'})

            TextStr = []

            # Append each line to the list
            for line in lyrictxt:
                TextStr.append(line.text)

            LyricsText.append(' '.join(TextStr))
        
        return LyricsText[0]
    
    except UnboundLocalError:
        return 'Not Found'