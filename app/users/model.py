class Users:

    def __init__(self, first_name, last_name,  email, birth_date, password, user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.password = password
        self.user_id = user_id

class Friends:

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id
