from app.messages.model import PrivateMessages, GroupMessages
from app.utils.database import get_connection


class PrivateMessagesService:

    @staticmethod
    def save(message: PrivateMessages):
        conn, cursor = get_connection()
        query = ('insert into private_message '
                 '(sender_id, recipient_id, date_sending, text_message) values (%s, %s, %s, %s)')
        values = (message.sender_id, message.recipient_id, message.date_sending, message.text_message)
        cursor.execute(query, values)
        conn.commit()


class PublicMassagesService:
    @staticmethod
    def save(message: GroupMessages):
        conn, cursor = get_connection()
        query = 'insert into group_massages (sender_id, date_sending, text_message) values (%s, %s, %s)'
        values = (message.sender_id, message.date_sending, message.text_message)
        cursor.execute(query, values)
        conn.commit()
