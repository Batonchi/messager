from psycopg2._psycopg import cursor

from app.users.model import Friends, Users
from database import get_connection


class UserService:
    @staticmethod
    def save(user: Users):
        conn, cursor = get_connection()
        query = ('insert into users (first_name, last_name, email, birth_date, photo_of_profile, password)'
                 'values (%s, %s, %s, %s, %s, %s)')
        values = (user.first_name, user.last_name, user.email, user.birth_date, str(user.photo_of_profile), user.password)
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
        user = Users(result[1], result[2], result[3], result[4], result[5], result[6], None, result[0])
        return user

    @staticmethod
    def find_by_any(search, user_Id):
        conn, cursor = get_connection()
        search_words = search.split()
        values = []
        query = 'select * from users left join friends on friends.user_id = users.user_id where ('
        for word in search_words:
            query += '(first_name ILIKE %s or last_name ILIKE %s) or '
            values.extend(['%' + word + '%', '%' + word + '%'])
        query = query[: -3]
        query += ") AND users.user_id != %s"
        values.extend([user_Id])
        print(query)
        cursor.execute(query, values)
        results = cursor.fetchall()
        users = [Users(result[1], result[2], result[3], result[4], result[5], result[6], None, result[0])
                 for result in results]
        return users
        

class FriendService:
    @staticmethod
    def save(user_id: int, friend_id: int):
        conn, cursor = get_connection()
        query = 'insert into friends (user_id, friend_id) values (%s, %s) on conflict (user_id, friend_id) do nothing'
        values = (user_id, friend_id)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def find_all(user_id: int):
        conn, cursor = get_connection()
        query = 'select * from friends where user_id=%s'
        values = (user_id,)
        cursor.execute(query, values)

    @staticmethod
    def delete(user_id: int, friend_id: int):
        conn, cursor = get_connection()
        query = 'delete from friends where user_id=%s and friend_id=%s'
        values = (user_id, friend_id)
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

    @staticmethod
    def accept(friend_id: int, user_id: int):
        conn, cursor = get_connection()
        query = '''UPDATE notification SET accept = 'true' WHERE user_id=%s AND friend_id=%s'''
        values = (user_id, friend_id)
        cursor.execute(query, values)
        conn.commit()