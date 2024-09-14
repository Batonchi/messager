from app.messages.model import PrivateMessages, PublicMessages
from app.utils.database import get_connection


class PrivateMessagesService:

    @staticmethod
    def save(message: PrivateMessages):
        conn, cursor = get_connection()
        query = ('insert into privatemessages '
                 '(sender_id, recipient_id, date_sending, text_messages) values (%s, %s, %s, %s)')
        values = (message.sender_id, message.recipient_id, message.date_sending, message.text_messages)
        cursor.execute(query, values)
        conn.commit()


class PublicMassagesService:
    @staticmethod
    def save(message: PublicMessages):
        conn, cursor = get_connection()
        query = 'insert into publicmassages (sender_id, date_sending, text_messages) values (%s, %s, %s)'
        values = (message.sender_id, message.date_sending, message.text_messages)
        cursor.execute(query, values)
        conn.commit()
