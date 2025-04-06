from psycopg2._psycopg import cursor
from datetime import date
from app.users.model import Users
from database import get_connection
from constant import FRIEND

from fastapi import WebSocket


class UserService:
    @staticmethod
    def save(user: Users):
        conn, cursor = get_connection()
        query = ('insert into users (first_name, last_name, email, birth_date, photo_of_profile, password)'
                 'values (%s, %s, %s, %s, %s, %s)')
        values = (
        user.first_name, user.last_name, user.email, user.birth_date, str(user.photo_of_profile), user.password)
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
    def find_by_id(user_id: int):
        conn, cursor = get_connection()
        query = 'select * from users where user_id=%s'
        values = (user_id,)
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

    @staticmethod
    def update(user_id: int, first_name: str, last_name: str, email: str, birth_date: date, about: str = ''):
        conn, cursor = get_connection()
        query = 'UPDATE users SET first_name=%s, last_name=%s, email=%s, birth_date=%s, about=%s WHERE user_id=%s'
        values = (first_name, last_name, email, birth_date, about, user_id)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()


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
        query = '''select users.user_id, first_name, last_name, email, users.birth_date, photo_of_profile from friends  
                    join users on friends.friend_id = users.user_id
                    where friends.user_id = %s'''
        values = (user_id,)
        cursor.execute(query, values)
        results = cursor.fetchall()
        users = [Users(result[1], result[2], result[3], result[4], result[5], user_id=result[0])
                 for result in results]
        return users

    @staticmethod
    def delete(user_id: int, friend_id: int):
        conn, cursor = get_connection()
        query = 'delete from friends where user_id=%s and friend_id=%s'
        values = (user_id, friend_id)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def check_friend(friend_id: int, user_id: int):
        conn, cursor = get_connection()
        query = '''SELECT * FROM friends WHERE user_id=%s AND friend_id=%s'''
        cursor.execute(query, (user_id, friend_id))
        results = cursor.fetchone()
        if results:
            return FRIEND.YES
            
        query = '''SELECT accept FROM notification WHERE user_id=%s AND friend_id=%s'''
        cursor.execute(query, (user_id, friend_id))
        results = cursor.fetchone()
        if results and not results[0]:
            return FRIEND.FROM
        
        query = '''SELECT accept FROM notification WHERE user_id=%s AND friend_id=%s'''
        cursor.execute(query, (friend_id, user_id))
        results = cursor.fetchone()
        if results and not results[0]:
            return FRIEND.FOR

        return FRIEND.NOT


class NotificationService:
    @staticmethod
    def save(friend_id: int, user_id: int):
        conn, cursor = get_connection()
        query = 'insert into notification (user_id, friend_id) values (%s, %s)'
        values = (user_id, friend_id)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def accept(friend_id: int, user_id: int):
        conn, cursor = get_connection()
        query = '''UPDATE notification SET accept = 'true' WHERE user_id=%s AND friend_id=%s'''
        values = (user_id, friend_id)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def find_all(friend_id: int = None, user_id: int = None):
        conn, cursor = get_connection()
        print(friend_id)
        if friend_id:
            cursor.execute('''SELECT users.user_id, users.first_name, users.last_name, users.photo_of_profile FROM notification JOIN users ON notification.user_id = users.user_id
                     WHERE notification.friend_id = %s AND notification.accept = 'false' ''', (friend_id,))
        elif user_id:
            cursor.execute('''SELECT users.user_id, users.first_name, users.last_name, users.photo_of_profile FROM notification JOIN users ON notification.friend_id = users.user_id
                     WHERE notification.user_id = %s AND notification.accept = 'false' ''', (user_id,))
        else:
            return
        users = [Users(result[1], result[2], photo_of_profile=result[3], user_id=result[0])
                 for result in cursor.fetchall()]
        return users


class ConnectionNotificationManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_notification(self, friend_id: int):
        websocket = self.active_connections.get(friend_id)
        if websocket:
            await websocket.send_text(str(friend_id))


con_manager = ConnectionNotificationManager()
