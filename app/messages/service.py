from app.messages.model import PrivateMessages, GroupMessages
from database import get_connection
from fastapi import WebSocket

class PrivateMessagesService:

    @staticmethod
    def save(sender_id, recipient_id, text_message):
        conn, cursor = get_connection()
        query = ('insert into private_message '
                 '(sender_id, recipient_id, text_message) values (%s, %s, %s)')
        values = (sender_id, recipient_id, text_message)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def find_chat(user1_id: int, user2_id: int):
        conn, cursor = get_connection()
        query = 'select * from where (sender_id = %s and recipient_id = %s) or (sender_id = %s and recipient_id = %s)'
        values = (user1_id, user2_id, user2_id, user1_id)
        cursor.execute(query, values)
        results = cursor.fetchall()
        messages = []
        if not results:
            return messages
        messages = [PrivateMessages(result[1], result[2], result[3], result[4], result[0]) for result in results]
        return messages


class GroupMassagesService:
    @staticmethod
    def save(message: GroupMessages):
        conn, cursor = get_connection()
        query = 'insert into group_massages (sender_id, date_sending, text_message) values (%s, %s, %s)'
        values = (message.sender_id, message.date_sending, message.text_message)
        cursor.execute(query, values)
        conn.commit()



class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, sender_id: int, recipient_id: int):
        websocket = self.active_connections.get(recipient_id)
        if websocket:
            await websocket.send_text(str(sender_id))
        websocket = self.active_connections.get(sender_id)
        if websocket:
            await websocket.send_text(str(recipient_id))

con_manager = ConnectionManager()