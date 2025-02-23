class PrivateMessages:

    def __init__(self, private_message_id, sender_id, sender, text_message, date_sending):
        self.private_message_id = private_message_id
        self.sender_id = sender_id
        self.sender = sender
        self.date_sending = date_sending
        self.text_message = text_message


class GroupMessages:

    def __init__(self, sender_id, date_sending, text_message, group_message_id=None):
        self.group_message_id = group_message_id
        self.sender_id = sender_id
        self.date_sending = date_sending
        self.text_message = text_message
