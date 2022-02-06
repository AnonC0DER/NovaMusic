def Get_users_count():
    '''Get users count'''
    Counter = 0
    # Open file
    file = open('Members.txt', 'r')
    # Read file
    data = file.read()
    # Split each line
    users = data.split('\n')

    # Count users
    for user in users:
        if user:
            Counter += 1
        
    return Counter


def Write_userID(userid):
    '''Write user ID to txt file'''
        
    file = open('Members.txt', 'a')
    file.write(str(userid) + '\n')
    file.close()


def is_user(userid):
    '''If userid isn't in txt file return Flase else True'''
    file = open('Members.txt')
    checker = file.read()
    file.close()

    if str(userid) in checker:
        return True
    
    else:
        return False