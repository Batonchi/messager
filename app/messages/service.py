from app.messages.model import PrivateMessages, GroupMessages
from database import get_connection


class PrivateMessagesService:

    @staticmethod
    def save(message: PrivateMessages):
        conn, cursor = get_connection()
        query = ('insert into private_message '
                 '(sender_id, recipient_id, text_message) values (%s, %s, %s)')
        values = (message.sender_id, message.recipient_id, message.text_message)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def find_chat(user1_id: str, user2_id: str):
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
