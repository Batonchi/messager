from app.users.model import Friends, Users
from database import get_connection


class UserService:
    @staticmethod
    def save(user: Users):
        conn, cursor = get_connection()
        query = ('insert into users (first_name, last_name, email, birth_date, photo_of_profile, about, password) '
                 'values (%s, %s, %s, %s, %s, %s, %s)')
        values = (user.first_name, user.last_name, user.email, user.birth_date, user.photo_of_profile,
                  user.about, user.password)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def find_by_email_and_password(email, password):
        conn, cursor = get_connection()
        query = 'select * from users where email=%s and password=%s'
        values = (email, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if not result:
            return None
        user = Users(result[1], result[2], result[3], result[4], None, result[0])
        return user

    @staticmethod
    def find_by_any(search):
        conn, cursor = get_connection()
        search_words = search.split()
        values = []
        query = 'select * from users where '
        for word in search_words:
            query += '(firs_name ILIKE %s or last_name ILIKE %s) or '
            values.extend([word, word])
        query = query[: -3]
        cursor.execute(query, values)
        results = cursor.fetchall()
        users = [Users(result[1], result[2], result[3], result[4], None, result[0]) for result in results]
        return users


class FriendService:
    @staticmethod
    def save(friend: Friends):
        conn, cursor = get_connection()
        query = 'insert into friends (user_id, friend_id) values (%s, %s)'
        values = (friend.user_id, friend.friend_id)
        cursor.execute(query, values)
        conn.commit()


class NotificationService:
    @staticmethod
    def save(friend: Friends):
        conn, cursor = get_connection()
        query = 'insert into notification (user_id, friend_id) values (%s, %s)'
        values = (friend.user_id, friend.friend_id)
        cursor.execute(query, values)
        conn.commit()