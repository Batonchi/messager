from pydantic import BaseModel
from datetime import date

class Users():

    def __init__(self, first_name, last_name,  email, birth_date, password=None, user_id=None):
        if user_id:
            self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        if password:
            self.password = password

class UsersForm(BaseModel):

    user_id: int = None
    first_name: str
    last_name: str
    email: str
    birth_date: date
    password: str 


class Friends:

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id
