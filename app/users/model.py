class Users:

    def __init__(self, first_name, last_name,  email=None, birth_date=None, photo_of_profile=None, about=None, password=None,
                 user_id=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.photo_of_profile = photo_of_profile
        self.about = about
        self.password = password
