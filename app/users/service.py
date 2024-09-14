from app.users.model import Friends, Passwords, Users
from app.utils.database import get_connection


class UserService:
    @staticmethod
    def save(user: Users):
        conn, cursor = get_connection()
        query = 'insert into users (first_name, last_name, email, birth_date, password) values (%s, %s, %s, %s, %s)'
        values = (user.first_name, user.last_name, user.email, user.birth_date, user.password)
        cursor.execute(query, values)
        conn.commit()


class FriendService:
    @staticmethod
    def save(friend: Friends):
        conn, cursor = get_connection()
        query = 'insert into friends (friend_1, friend_2) values (%s, %s)'
        values = (friend.friend_1, friend.friend_2)
        cursor.execute(query, values)
        conn.commit()