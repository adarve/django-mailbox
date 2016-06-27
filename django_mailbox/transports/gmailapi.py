  GNU nano 2.2.6                                   File: /home/ubuntu/Envs/peanutbutter/local/lib/python2.7/site-packages/django_mailbox/transports/gmailapi.py                                                                              

from .base import EmailTransport, MessageParseError
import server_side_gmail
import base64
import email


class GmailAPITransport(EmailTransport):
    def __init__(self):
        self.username = None
        self.user_id = None
        self.watch_address = None
        self.http = None
        self.credentials = None
        self.service = None

    #Watch request. Set up or update a push notification watch on the given user mailbox.
    def watch(self):
        self.request = { 'labelIds': ['INBOX'],  'topicName': str(self.watch_address)}
        self.service.users().watch(userId='me', body=self.request).execute()


    def connect(self, username, user_id, watch_address):
        self.username = username
        self.user_id = user_id
        self.watch_address = watch_address[1:]

        try:
            self.credentials = server_side_gmail.get_gmail_credentials(user_id)
        except Exception, error:
            print ('An error occurred loading the credentials. You have to execute create_credential.py file to create it. ' + error)
            return None

        self.http = self.credentials.authorize(server_side_gmail.httplib2.Http())
        self.service = server_side_gmail.discovery.build('gmail', 'v1', http=self.http)





    def get_message(self, condition=None):
        messages_list = self.service.users().messages().list(userId='me', q="is:unread").execute()

        if "messages" in messages_list:
            for message_gmail in messages_list["messages"]:
                try:
                    message_api_gmail = self.service.users().messages().get(userId='me', id=message_gmail["id"], format='raw').execute()

                    msg_str = base64.urlsafe_b64decode(message_api_gmail['raw'].encode('utf-8','ignore'))

                    msg = email.message_from_string(msg_str.decode('ascii','ignore'))

                    if condition and not condition(msg):
                        continue

                    """
                    Main labels:
                    INBOX, SPAM, TRASH, UNREAD, STARRED, IMPORTANT, SENT, DRAFT
                    """
                    msg_labels = { "addLabelIds": [],"removeLabelIds": ['UNREAD', 'INBOX']}
                    self.service.users().messages().modify(userId='me', id=message_gmail["id"],  body=msg_labels).execute()

                    yield msg

                except MessageParseError:
                    continue
        return


