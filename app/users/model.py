from fastapi import UploadFile
from pydantic import BaseModel
from datetime import date


class Users:

    def __init__(self, first_name, last_name,  email, birth_date, photo_of_profile=None, about=None, password=None,
                 user_id=None):
        if user_id:
            self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        if photo_of_profile:
            self.photo_of_profile = photo_of_profile
        if about:
            self.about = about
        if password:
            self.password = password


class UsersForm(BaseModel):

    user_id: int = None
    first_name: str
    last_name: str
    email: str
    birth_date: date
    photo_of_profile: UploadFile = None
    about: str = None
    password: str 


class Friends:

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id
