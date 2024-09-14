class Users:

    def __init__(self, first_name, last_name,  email, birth_date, password, user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.password = password
        self.user_id = user_id


class Passwords:

    def __init__(self, pass_text, password_id=None):
        self.pass_text = pass_text
        self.password_id = password_id


class Friends:

    def __init__(self, friend_1, friend_2, friend_id=None):
        self.friend_1 = friend_1
        self.friend_2 = friend_2
        self.friend_id = friend_id