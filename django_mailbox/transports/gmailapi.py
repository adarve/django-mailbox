from django.conf import settings

from .base import EmailTransport, MessageParseError
import server_side_gmail

import base64
import json

class GmailAPITransport(EmailTransport):
    def __init__(self):
        self.username = None
        self.user_id = None
        self.watch_address = None

    def connect(self, username, user_id, watch_address):
        self.username = username
        self.user_id = user_id
        self.watch_address = watch_address[1:]

        request = { 'labelIds': ['INBOX'],  'topicName': watch_address }

        credentials = server_side_gmail.get_gmail_credentials(user_id)

        http = credentials.authorize(server_side_gmail.httplib2.Http())

        service = server_side_gmail.discovery.build('gmail', 'v1', http=http)
        service.users().watch(userId='me', body=request).execute()

    def get_message(self, condition=None):
        messages_list = service.users().messages().list(userId='me', q="is:unread").execute()

        if "messages" in messages_list:
            try:
                for message_gmail in messages_list["messages"]:
                    message_api_gmail = service.users().messages().get(userId='me', id=message_gmail["id"], format='raw').execute()

                    msg_str = base64.urlsafe_b64decode(message_api_gmail['raw'].encode('utf-8','ignore'))

                    msg = email.message_from_string(msg_str.decode('ascii','ignore'))


                    if condition and not condition(msg):
                        continue

                    yield msg

                    """
                    Main labels:
                    INBOX, SPAM, TRASH, UNREAD, STARRED, IMPORTANT, SENT, Draft
                    """
                    msg_labels = { "addLabelIds": [],"removeLabelIds": ['UNREAD', 'INBOX']}
                    service.users().messages().modify(userId='me', id=message_gmail["id"],  body=msg_labels).execute()
                except MessageParseError:
                    continue
        return
