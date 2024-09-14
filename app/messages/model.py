class PrivateMessages:

    def __init__(self, sender_id, recipient_id, date_sending, text_messages, private_message_id=None):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.date_sending = date_sending
        self.text_messages = text_messages
        self.private_message_id = private_message_id


class GroupMessages:

    def __init__(self, sender_id, date_sending, text_messages, public_message_id=None):
        self.sender_id = sender_id
        self.date_sending = date_sending
        self.text_messages = text_messages
        self.public_message_id = public_message_id